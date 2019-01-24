import sys


# Input: Lidar txt form
# Output: RbnnResult for r=3 with all values -1

# Args: [1] = Lidar txt path, [2] = rbnn result to save path, [3] int number to put per line

if __name__ == "__main__":

    if (len(sys.argv) != 4):
        print('NOT ENOUGH ARGUMENTS')
        exit(1)

    file_lidar_txt = sys.argv[1]
    file_dest = sys.argv[2]
    number_per_line = sys.argv[3]

    a = open(file_lidar_txt, 'r').readlines()
    a = [number_per_line for l in a]
    open(file_dest, 'w').write(''.join(a))