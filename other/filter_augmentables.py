import sys


# Input: Lidar txt form
# Output: RbnnResult for r=3 with all values -1

# Args: [1] = Lidar txt path, [2] = rbnn result to save path

if __name__ == "__main__":

    if (len(sys.argv) != 3):
        print('NOT ENOUGH ARGUMENTS')
        exit(1)

    file = sys.argv[1]
    resfile = sys.argv[2]

    a = open(file, 'r').readlines()
    a = [l for l in a if l[-2] != '0']
    open(resfile, 'w').write(''.join(a))