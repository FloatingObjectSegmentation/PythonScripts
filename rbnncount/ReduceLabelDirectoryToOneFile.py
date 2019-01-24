import os

dataset_name = '459_100'
folder = 'C:\\Users\\km\\Desktop\\MAG\\FloatingObjectFilter\\data\\459_\\labels'

files = [folder + '\\' + f for f in os.listdir(folder) if f.startswith(dataset_name)]
final_string = ''
for f in files:
    final_string = final_string + ' '.join([line.rstrip("\n") for line in open(f, 'r').readlines()]) + '\n'
open(folder + '\\' + dataset_name + '_reduced.txt', 'w').write(final_string)