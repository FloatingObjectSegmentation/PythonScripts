import os
import numpy as np
import re
from collections import defaultdict


lidar_folder = 'E:\\workspaces\\LIDAR_WORKSPACE\\lidar'
labeling_folder = 'E:\\workspaces\\LIDAR_WORKSPACE\\lidar\\labels'
augmentations_folder = 'E:/workspaces/LIDAR_WORKSPACE/lidar/augmentation'
rbnn_val = 3
result_savefile = 'E:/workspaces/LIDAR_WORKSPACE/results/data'

use_labels = False


def is_lidar_file(filename):
    a = filename.split('_')
    return a[:-4] == '.txt' and len(a) == 11


# load the lidar file
files = [lidar_folder + '\\' + f for f in os.listdir(lidar_folder)]
pattern = '[0-9]{3}[_]{1}[0-9]{2,3}'
dataset_names = list(set([x.group(0) for x in [re.search(pattern, match, flags=0) for match in files] if x != None]))
dataset_names.sort()

for dataset_name in dataset_names:

    # fill up X
    points = [line.rstrip('\n') for line in open(lidar_folder + '\\' + dataset_name + '.txt').readlines()]
    X = np.zeros((len(points), 3))
    for i in range(len(points)):
        a = points[i].split(' ')
        X[i, :] = np.array([float(a[0]), float(a[1]), float(a[2])])

    # prepare targets
    y = np.zeros(len(points))

    # load augmentations
    aug_files = [augmentations_folder + '\\' + f for f in os.listdir(augmentations_folder) if f.find(dataset_name) != -1]
    if len(aug_files) == 0:
        continue # for the current dataset, there were no augmentations found
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
    points = [x for x in points if x != ''] # get rid of augmentations that the lidar did not hit at all
    points = [[tuple([float(z[2:]) for z in y.split(' ')]) for y in x.split(',')] for x in points]

    # zip these together
    aug_pts_and_dists = [(float(x),y) for x,y in zip(rbnn_vals, points)] # only take the augs above the desired threshold

    # get all of the points so you know how large X_augs will be
    all_aug_pts_len = sum([len(ps) for ps in points])
    X_augs = np.zeros((all_aug_pts_len, 3))

    # fill up X_augs
    curr_idx = 0
    for dist, aug in aug_pts_and_dists:
        for pt in aug:
            X_augs[curr_idx][:] = np.array([pt[0], pt[1], pt[2]])
            curr_idx += 1


    # construct final matrix
    print('saving ' + dataset_name)
    y_augs = np.ones(X_augs.shape[0])
    X = np.concatenate((X, X_augs))
    y = np.concatenate((y, y_augs))
    X = np.concatenate((X, y[:, None]), axis=1)
    np.save(result_savefile + dataset_name + '.npy', X, True, True)

