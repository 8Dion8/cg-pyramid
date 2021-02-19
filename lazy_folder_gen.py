import os, shutil

dir_name = "/Users/glebsvarcer/Desktop/cg-pyramid/fonts/"
files = os.listdir(dir_name)

for i in files:
    try:
        os.mkdir(os.path.join(dir_name , i.split(".")[0]))
        shutil.copy(os.path.join(dir_name , i), os.path.join(dir_name , i.split(".")[0]))
    except:pass