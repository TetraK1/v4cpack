import os
for dirpath, dirnames, fnames in os.walk('./'):
    print(len(fnames), len(dirnames), dirpath, sep='\t')