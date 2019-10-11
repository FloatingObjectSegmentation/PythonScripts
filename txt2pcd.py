def numpymat_to_pcd(X, filepath):

    header = "# .PCD v.7 - Point Cloud Data file format" + "\n"
    header += "VERSION .7" + "\n"
    header += "FIELDS x y z" + "\n"
    header += "SIZE 4 4 4" + "\n"
    header += "TYPE F F F" + "\n"
    header += "COUNT 1 1 1" + "\n"
    header += f"WIDTH {X.shape[0]}" + "\n"
    header += "HEIGHT 1" + "\n"
    header += "VIEWPOINT 0 0 0 1 0 0 0" + "\n"
    header += f"POINTS {X.shape[0]}" + "\n"
    header += "DATA ascii" + "\n"

    file =  open(filepath, 'w')
    file.write(header)
    for i in range(X.shape[0]):
        file.write("{0:.5f}".format(X[i,0]) + ' ' + "{0:.5f}".format(X[i,1]) + ' ' + "{0:.5f}".format(X[i,2]) + '\n')