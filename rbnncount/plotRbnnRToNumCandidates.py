import pylab as pl
import numpy as np

hsh = {'3': [494, 982, 924, 696, 1296, 794, 1395, 1519, 482], '1': [94037, 468103, 89157, 96628, 393349, 96781, 120338, 228091, 88438], '2': [3213, 14926, 3179, 3145, 15170, 2881, 5428, 9768, 2443], '4': [130, 84, 428, 195, 166, 340, 468, 428, 177], '5': [43, 13, 166, 51, 38, 158, 206, 152, 77], '8': [6, 2, 22, 11, 8, 24, 37, 31, 9]}

arr = list(hsh.keys())
arr.sort()
means  = [np.mean(hsh[k]) for k in arr][2:]
means = [k / means[0] for k in means]
#stdevs = [np.log10(np.std(hsh[k])) for k in arr]
x = [float(k) for k in arr][2:]

pl.plot(x, means, 'r', label='mean')
#pl.plot(x, stdevs, 'b', label='stdev')
pl.xlabel('RBNN radius r')
pl.ylabel('Proportion of candidates with respect to r=3')
pl.title("Characteristics of 10 pieces of 1km^2 squares of Slovenia's terrain")
pl.legend(loc='upper right')
pl.show()