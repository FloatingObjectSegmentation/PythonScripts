import os.path
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
from collections import defaultdict

directory = 'C:\\Users\\km\\Desktop\\MAG\\FloatingObjectFilter\\data'


def computeNumUniqueClusters(parts):

    neki = set()
    for p in parts[1:]:
        neki.add(p)
    return len(neki)



def getCandidateNumbers():
    filenames = [directory + '/' + f for f in listdir(directory) if isfile(directory + "/" + f) and f.find('result') != -1]

    resultmap = defaultdict(list)

    for f in filenames:
        lines = open(f, 'r').readlines()
        for line in lines:
            line = line[:-2]
            resultmap[line[0]].append((f, computeNumUniqueClusters([float(x) for x in line.split(' ')])))
            print(line[0] + ": " + str(resultmap[line[0]]))
    return resultmap