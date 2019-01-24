file1 = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121augslidarlidarmerge'
filedest = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121rbnn'

a = open(file1, 'r').readlines()
a = ['-1' for l in a]
open(filedest, 'w').write('3 ' + ' '.join(a))