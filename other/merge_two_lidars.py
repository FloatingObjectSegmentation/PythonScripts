file1 = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121augslidar'
file2 = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121rm'
filedest = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121augslidarlidarmerge'

a = open(file1, 'r').read()
b = open(file2, 'r').read()
open(filedest, 'w').write(a + "\n" + b)