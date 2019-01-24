file = 'E:/workspaces/LIDAR_WORKSPACE/dmr/449_121rm'
resfile = 'E:/workspaces/LIDAR_WORKSPACE/dmr/449_121rm'
a = open(file, 'r').readlines()
a = [l for l in a if l[-2] != '0']
open(resfile, 'w').write(''.join(a))