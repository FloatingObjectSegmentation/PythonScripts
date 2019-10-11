import os
import numpy as np
import re
import subprocess
import txt2pcd
import time
import pickle
from collections import defaultdict
import multiprocessing as mp

lidar_folder = 'E:\\workspaces\\LIDAR_WORKSPACE\\lidar'
augmentations_folder = 'E:/workspaces/LIDAR_WORKSPACE/lidar/augmentation'

savefolder = 'E:\\workspaces\\LIDAR_WORKSPACE\\temp'

rbnnpath = "C:\\Users\\km\\Desktop\\playground\\LazPreprocessor\\external_tools\\resources"
rbnn_vals = [2, 3, 4, 5, 6, 7, 8, 9, 10]

def is_lidar_file(filename):
    a = filename.split('_')
    return a[:-4] == '.txt' and len(a) == 11

def partition_list(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def load_points_lidar_dataset(dataset_name):
    points = [line.rstrip('\n') for line in open(lidar_folder + '\\' + dataset_name + '.txt').readlines()]
    X = np.zeros((len(points), 3))
    for i in range(len(points)):
        a = points[i].split(' ')
        X[i, :] = np.array([float(a[0]), float(a[1]), float(a[2])])
    return X

def load_points_augs_dataset(dataset_name):

    aug_files = [augmentations_folder + '\\' + f for f in os.listdir(augmentations_folder) if
                 f.find(dataset_name) != -1]
    if len(aug_files) == 0:
        return None
    aug_file = aug_files[0]

    # get the [2] parameter - rbnn r
    augs = open(aug_file, 'r').readlines()
    rbnn_vals = [a.split(' ')[2] for a in augs]

    # get the [3] parameter - XYZ points
    points = []
    for a in augs:
        idx1 = a.find('[')
        idx2 = a.find(']')
        points.append(a[idx1 + 1:idx2])
    points = [x for x in points if x != '']  # get rid of augmentations that the lidar did not hit at all
    points = [[tuple([float(z[2:]) for z in y.split(' ')]) for y in x.split(',')] for x in points]

    # zip these together
    aug_pts_and_dists = [(float(x), y) for x, y in
                         zip(rbnn_vals, points)]  # only take the augs above the desired threshold

    # get all of the points so you know how large X_augs will be
    all_aug_pts_len = sum([len(ps) for ps in points])
    X_augs = np.zeros((all_aug_pts_len, 3))

    # fill up X_augs
    curr_idx = 0
    for dist, aug in aug_pts_and_dists:
        for pt in aug:
            X_augs[curr_idx][:] = np.array([pt[0], pt[1], pt[2]])
            curr_idx += 1
    return X_augs

class OneDatasetWork:

    def __init__(self, name):
        self.name = name
    def work(self):

        name = self.name

        print("LOADING RAW DATA")
        X_orig, X_augs = None, None
        npypickle = f'{savefolder}/{name}.npy'
        if not os.path.isfile(npypickle):
            X_orig = load_points_lidar_dataset(name)
            X_augs = load_points_augs_dataset(name)
            pickle.dump((X_orig, X_augs), open(npypickle, 'wb'))
        else:
            X_orig, X_augs = pickle.load(open(npypickle, 'rb'))
        X = np.concatenate((X_orig, X_augs))

        print("ATTEMPT CREATING PCD")
        start = time.time()
        savefile = f'{savefolder}/{name}.pcd'
        if not os.path.isfile(savefile):
            txt2pcd.numpymat_to_pcd(X, savefile)
        end = time.time()
        print("txt2pcd time: " + str(end - start))

        print("ATTEMPTING RBNN")
        rbnnresultfile = f'{savefolder}/rbnnresult{name}.pcd'
        if not os.path.isfile(rbnnresultfile):
            args = []
            args.append(f'{rbnnpath}/rbnn.exe')
            args.append(savefolder)
            args.append(f'{name}.pcd')
            args.append('rbnnresult')
            for r in rbnn_vals:
                args.append(str(r))
            subprocess.run(args)

if __name__ == '__main__':
    # load the lidar file
    files = [lidar_folder + '\\' + f for f in os.listdir(lidar_folder)]
    pattern = '[0-9]{3}[_]{1}[0-9]{2,3}'
    dataset_names = list(set([x.group(0) for x in [re.search(pattern, match, flags=0) for match in files] if x != None]))
    dataset_names.sort()


    # Compute results using multiprocessing
    partition = partition_list(dataset_names, 5)
    for chunk in partition:

        wrk = [OneDatasetWork(x) for x in chunk]
        thr = [mp.Process(target=x.work, args=()) for x in wrk]

        for i in range(len(wrk)):
            thr[i].start()

        for i in range(len(wrk)):
            thr[i].join()

    # aggregate the results
    rbnnval_to_confmat = defaultdict(defaultdict(int))
    for name in dataset_names:

        print("READINGRBNNRESULTS")
        rbnnresultfile = f'{savefolder}/rbnnresult{name}.pcd'
        results = open(rbnnresultfile, 'r').readlines()
        for line in results:

            parts = line.split(' ')
            rbnnval = parts[0]
            preds = [int(x) > 0 for x in parts[1:]]
            for i in range(len(preds)):

                gtru = 1 if i > X_orig.shape[0] else 0
                pred = 1 if preds[1] > 0 else 0

                if gtru == 0 and pred == 0:
                    rbnnval_to_confmat[rbnnval]['TN'] += 1
                if gtru == 0 and pred == 1:
                    rbnnval_to_confmat[rbnnval]['FP'] += 1
                if gtru == 1 and pred == 0:
                    rbnnval_to_confmat[rbnnval]['FN'] += 1
                if gtru == 1 and pred == 1:
                    rbnnval_to_confmat[rbnnval]['TP'] += 1
