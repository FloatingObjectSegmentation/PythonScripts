import numpy as np

originals_folder = 'E:/workspaces/LIDAR_WORKSPACE/results'
rbnnres_folder = 'E:/workspaces/LIDAR_WORKSPACE/temp'
spgres_folder = 'E:/workspaces/LIDAR_WORKSPACE/spgresults'
test_chunk = '614_154'

outputfolder = 'E:/workspaces/LIDAR_WORKSPACE/visdata'

# load original augmented data labels
# ORIGIGI = workspace/results/
ORIGIGI = np.load(open(originals_folder + '/data' + test_chunk + '.npy', 'rb'))

# load RBNN results
# RBNNRES = workspace/temp/
# take r=5 because F1 score is minimal there.
RBNNRES = open(rbnnres_folder + '/rbnnresult' + test_chunk + '.pcd', 'r').readlines()
RBNNRES = np.array([int(a) for a in RBNNRES[4].split(' ')[1:-1]])
RBNNRES[np.where(RBNNRES == -1)] = 0
RBNNRES[np.where(RBNNRES > 0)] = 1


# load SPG results
# SPGRES = first save them into workspace/spgresults
SPGRES = np.load(open(spgres_folder + '/data' + test_chunk + '.npy', 'rb'))

# merge ORIGIGI, RBNNRES, SPGRES
X = np.concatenate((np.asmatrix(ORIGIGI[:, 3]).T, np.asmatrix(RBNNRES).T, np.asmatrix(SPGRES).T), axis=1)
Y = X.dot(np.array([4, 2, 1]))
Y = np.asarray(Y)

# WRITE LABELS
a = '\n'.join([str(int(Y[0, i])) for i in range(max(Y.shape))])
open(outputfolder + '/' + test_chunk + 'class.txt', 'w').write(a)

# TRANSFORM ORIGIGI XYZ INTO TXT FORMAT, SAVE TO workspace/resultvis
X = ORIGIGI
a = '\n'.join(["{0:.5f}".format(X[i,0]) + ' ' + "{0:.5f}".format(X[i,1]) + ' ' + "{0:.5f}".format(X[i,2]) + ' 0 0 0' for i in range(max(ORIGIGI.shape))])
open(outputfolder + '/' + test_chunk + '.txt', 'w').write(a)
