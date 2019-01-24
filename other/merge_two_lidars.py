import sys

# Input: Lidar txt form
# Output: RbnnResult for r=3 with all values -1

# Args: [1] = Lidar txt path, [2] = rbnn result to save path

if __name__ == "__main__":

    if (len(sys.argv) != 4):
        print('NOT ENOUGH ARGUMENTS')
        exit(1)


    file1 = sys.argv[1]
    file2 = sys.argv[2]
    filedest = sys.argv[3]

    a = open(file1, 'r').read()
    b = open(file2, 'r').read()
    open(filedest, 'w').write(a + "\n" + b)

file1 = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121augslidar'
file2 = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121rm'
filedest = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121augslidarlidarmerge'