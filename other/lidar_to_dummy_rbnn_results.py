import sys


# Input: Lidar txt form
# Output: RbnnResult for r=3 with all values -1

# Args: [1] = Lidar txt path, [2] = rbnn result to save path

if __name__ == "__main__":

    if (len(sys.argv) != 3):
        print('NOT ENOUGH ARGUMENTS')
        exit(1)

    file_lidar_txt = sys.argv[1]
    file_dest = sys.argv[2]

    a = open(file_lidar_txt, 'r').readlines()
    a = ['-1' for l in a]
    open(file_dest, 'w').write('3 ' + ' '.join(a))