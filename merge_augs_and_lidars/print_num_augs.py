import os
import numpy as np
import re
from collections import defaultdict

# Made to verify that there are the same number of augmentations lines as there are augmentables lines

augmentations_folder = 'E:/workspaces/LIDAR_WORKSPACE/lidar/augmentation'
augmentables_folder = 'E:\\workspaces\\LIDAR_WORKSPACE\\augmentation\\augmentables_experiment1_finalsolution'

use_labels = False

def is_lidar_file(filename):
    a = filename.split('_')
    return a[:-4] == '.txt' and len(a) == 11


# load the lidar file
files = [augmentations_folder + '\\' + f for f in os.listdir(augmentations_folder)]
pattern = '[0-9]{3}[_]{1}[0-9]{2,3}'
dataset_names = list(set([x.group(0) for x in [re.search(pattern, match, flags=0) for match in files] if x != None]))
dataset_names.sort()

for name in dataset_names:

    # load augmentations
    aug_files = [augmentations_folder + '\\' + f for f in os.listdir(augmentations_folder) if
                 f.find(name) != -1]
    if len(aug_files) == 0:
        continue  # for the current dataset, there were no augmentations found
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

    lines = open(augmentations_folder + '//' + name + 'AUGSFINAL', 'r').readlines()
    lines1 = open(augmentables_folder + '//' + name + '.txt', 'r').readlines()
    print(name + ' ' + str(len(lines)) + ' ' + str(len(lines1)) + ' ' + str(len(points)))
