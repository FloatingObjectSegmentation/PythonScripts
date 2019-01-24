import sys
from random import randint
# Input: Lidar TXT file, PBBMDF file
# Output: PBBMDF all points including bbox vertices transformed to lidar file's space, to Lidar format:
#            x y z 0 0 0
#            x y z 0 0 0 ...

# Args:
#       [1] = Lidar TXT file path
#       [2] = PBBMDF
#       [3] = destination save file path
#       [4] = if 0, then we add the minimum point of the lidar to each sample in PBBMDF



def rndstring():
    return ' '.join([str(randint(0, 65000)) for l in range(3)])

if __name__ == "__main__":

    if (len(sys.argv) != 5):
        print('NOT ENOUGH ARGUMENTS')
        exit(1)

    file_lidar = sys.argv[1]
    file_pbbmdf = sys.argv[2]
    savefile = sys.argv[3]

    # original
    a = open(file_lidar, 'r').readlines()
    a = [l.split(" ") for l in a]
    minx = min([float(l[0]) for l in a])
    miny = min([float(l[1]) for l in a])
    minz = min([float(l[2]) for l in a])

    # augs
    aug = open(file_pbbmdf, 'r').readlines()
    aug = [l.split(" ") for l in aug]
    aug = [[b.split(",") for b in l] for l in aug]
    aug = [[" ".join(
        [str(float(b[0]) + (minx if sys.argv[4] == '0' else 0)),
         str(float(b[1]) + (miny if sys.argv[4] == '0' else 0)),
         str(float(b[2]) + (minz if sys.argv[4] == '0' else 0))]
    ) + " " + rndstring() for b in
            l[:-1]] for l in aug]
    aug = ["\n".join(l) for l in aug]

    open(savefile, 'w').write('\n'.join(aug))