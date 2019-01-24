import pylab as plt
import numpy as np
import os.path
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
from collections import defaultdict
import computeNumUniqueClustersForEachR as comp

import json

# config
dataset_names = ['459_101', '459_99', '461_101']

# auxiliary methods

def getStringThatItemMatches(item, searchstrings):
    for src in searchstrings:
            if item.find(src) != -1:
                return src
    return ''

def getMapOfRbnnRAndDatasetNameToNumCandidates():
    resultmap = comp.getCandidateNumbers()
    searchstrings = dataset_names

    filtered = {}
    for k in resultmap.keys():
        value = resultmap[k]
        # create hash[<rbnn_r>][<dataset_name>] = numcandidates
        filtered[k] = defaultdict(dict)

        dataset_numCandidates_pairs = [(getStringThatItemMatches(x[0], searchstrings), x[1]) for x in value if
                                       getStringThatItemMatches(x[0], searchstrings) != '']

        for pair in dataset_numCandidates_pairs:
            filtered[k][pair[0]] = pair[1]
    return filtered

def parseLabels(filename):
    # create a hashmap[<rbnn_r>][<label>] = candidate_count
    lines = open(filename, 'r').readlines()
    lines = [line.split(" ")for line in lines]
    result = defaultdict(lambda: defaultdict(int))
    for line in lines:
        result[line[1]][line[0]] += 1
    return result

def invertNumCandidatesHash(numcandidates_hash):
    # from [rbnn_r][dataset] -> [dataset][rbnn_r]
    result = defaultdict(lambda: defaultdict(int))
    for rbnn_r in numcandidates_hash.keys():
        for dataset in numcandidates_hash[rbnn_r].keys():
            result[dataset][rbnn_r] = numcandidates_hash[rbnn_r][dataset]
    return result

def correctNumberOfNegs(numcandidates_hash, labels):
    # correct the number of negative labels
    for dataset in labels.keys():
        for rbnn_r in labels[dataset].keys():
            count = numcandidates_hash[dataset][rbnn_r]
            poz = 0
            if '0' in labels[dataset][rbnn_r]:
                poz = labels[dataset][rbnn_r]['0']
            likely = 0
            if '1' in labels[dataset][rbnn_r]:
                likely = labels[dataset][rbnn_r]['1']
            maybe = 0
            if '2' in labels[dataset][rbnn_r]:
                maybe = labels[dataset][rbnn_r]['2']

            labels[dataset][rbnn_r]['3'] = count - poz - maybe - likely
    return labels

# code

if not isfile('numcandidates.json'):
    print('getting the candidates')
    rbnnrdsname_to_candidateNum = getMapOfRbnnRAndDatasetNameToNumCandidates()
    json.dump(rbnnrdsname_to_candidateNum, open('numcandidates.json', 'w'))

dirs = ['C:\\Users\\km\\Desktop\\MAG\\FloatingObjectFilter\\data\\461_\\labels\\', 'C:\\Users\\km\\Desktop\\MAG\\FloatingObjectFilter\\data\\459_\\labels\\']
paths = [dirs[0] + '461_101_reduced.txt', dirs[1] + '459_101_reduced.txt', dirs[1] + '459_99_reduced.txt']

if not isfile('labels.json'):
    print('getting the labels')
    hash = {}
    for path in paths:
        print(path)
        hash[getStringThatItemMatches(path, dataset_names)] = parseLabels(path)

    json.dump(hash, open('labels.json', 'w'))

## actual plotting

labels = json.load(open('labels.json', 'r'))
numcandidates_hash = json.load(open('numcandidates.json', 'r'))
numcandidates_hash = invertNumCandidatesHash(numcandidates_hash)
labels = correctNumberOfNegs(numcandidates_hash, labels)

plt.figure(1)
colors = dict(zip(dataset_names, ['r', 'g', 'b']))

def sumall(dataset, rbnn_r):
    # gets the sum of the candidates (number of candidates) for each rbnn_r and dataset
    return sum([labels[dataset][rbnn_r][label] if label in labels[dataset][rbnn_r] else 0 for label in ['3', '2', '1', '0']])

# negs
ax = plt.subplot(221)
for dataset in labels.keys():
    x = [3, 5, 8]
    y = [labels[dataset][rbnn_r]['3'] / labels[dataset]['3']['3'] for rbnn_r in sorted(labels[dataset].keys())]
    plt.plot(x,y, color=colors[dataset], label=dataset)
ax.title.set_text('Negative')
ax.legend(loc='upper right')
plt.xlabel('RBNN radius r')
plt.ylabel('recall')
# maybe
ax = plt.subplot(222)
for dataset in labels.keys():
    x = [3, 5, 8]
    y = [labels[dataset][rbnn_r]['2'] / labels[dataset]['3']['2'] if '2' in labels[dataset][rbnn_r] else 0 for rbnn_r in sorted(labels[dataset].keys())]
    plt.plot(x,y, color=colors[dataset], label=dataset)
ax.title.set_text('Maybe positive')
ax.legend(loc='upper right')
plt.xlabel('RBNN radius r')
plt.ylabel('recall')
# likely
ax = plt.subplot(223)
for dataset in labels.keys():
    x = [3, 5, 8]
    y = [labels[dataset][rbnn_r]['1'] / labels[dataset]['3']['1'] if '1' in labels[dataset][rbnn_r] else 0 for rbnn_r in sorted(labels[dataset].keys())]
    plt.plot(x,y, color=colors[dataset], label=dataset)
ax.title.set_text('Likely positive')
ax.legend(loc='upper right')
plt.xlabel('RBNN radius r')
plt.ylabel('recall')
# pos
ax = plt.subplot(224)

for dataset in labels.keys():
    x = [3, 5, 8]
    y = [labels[dataset][rbnn_r]['0'] / labels[dataset]['3']['0'] if '0' in labels[dataset][rbnn_r] else 0 for rbnn_r in sorted(labels[dataset].keys())]
    ax.plot(x,y, color=colors[dataset], label=dataset)
ax.title.set_text('Positive')
ax.legend(loc='upper right')
plt.xlabel('RBNN radius r')
plt.ylabel('recall')

plt.legend(loc='upper right')
plt.show()
