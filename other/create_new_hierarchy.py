import os
import datetime

root_dir = 'C:\\Users\\km\\Desktop\\integratables_backup\\Integratables\\'
destination = 'C:\\Users\\km\\Desktop\\integratables_backup\\NewIntegratables\\'

def rec_some(file):
    try:
        if (os.path.isdir(file)):
            for sub in os.listdir(file):
                rec_some(file + '\\' + sub)
        else:
            fullpath = os.path.abspath(file)
            lines = open(fullpath, 'r').readlines()
            lines = [f"{datetime.datetime.now():%Y-%m-%d} " + l if len(l) > 5 else l for l in lines]
            all = '\n'.join(lines)
            open(fullpath, 'w').write(all)
    except PermissionError:
        pass
