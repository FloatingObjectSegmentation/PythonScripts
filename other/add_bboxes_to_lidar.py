# Problem specification: Take the LIDAR file {file}, and a file of PointBoundingBoxAndMaxDimFormat augmentation
#                        samples.
#



# opens the lidar file, finds the max and mins, then from the PointBoundingBoxAndMaxDimFormat
# creates the lidar format, so the bounding boxes can be viewed in unreal engine

file = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121rm'
file_augs = 'E:/workspaces/LIDAR_WORKSPACE/test2/augs'
PointCloudBoxAndMaxDimFormatFileToLidarFormatDestinationFile = 'E:/workspaces/LIDAR_WORKSPACE/test2/449_121augslidar'


# origigi
a = open(file, 'r').readlines()
a = [l.split(" ") for l in a]
minx = min([float(l[0]) for l in a])
miny = min([float(l[1]) for l in a])
minz = min([float(l[2]) for l in a])

# augs
aug = open(file_augs, 'r').readlines()
aug = [l.split(" ") for l in aug]
aug = [[b.split(",") for b in l] for l in aug]
aug = [[ " ".join([str(float(b[0]) + minx), str(float(b[1]) + miny), str(float(b[2]) + minz)]) + " 0 0 0" for b in l[:-1]] for l in aug]
aug = ["\n".join(l) for l in aug]


open(PointCloudBoxAndMaxDimFormatFileToLidarFormatDestinationFile, 'w').write('\n'.join(aug))