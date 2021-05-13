import os 
"""
compare 2 file and show the different lines 
compare 2 folders show the file names are different 
"""
def diff_folder(dir1, dir2):
    dir1_folders = []
    dir1_files = []
    for dir, folders, file_names in os.walk(dir1):
        dir1_folders.extend([os.path.relpath(os.path.join(dir, f), dir1) for f in folders])
        dir1_files.extend([os.path.relpath(os.path.join(dir, f),dir1) for f in file_names])
    dir2_folders = []
    dir2_files = []
    for dir, folders, file_names in os.walk(dir2):
        dir2_folders.extend([os.path.relpath(os.path.join(dir, f), dir2) for f in folders])
        dir2_files.extend([os.path.relpath(os.path.join(dir, f), dir2) for f in file_names])
    dir1_only = set(dir1_folders) - set(dir2_folders)
    dir2_only = set(dir2_folders) - set(dir1_folders)
    file1_only = set(dir1_files) - set(dir2_files)
    file2_only = set(dir2_files) - set(dir1_files)
    print('=======folders only in dir1=======')
    for f in dir1_only:
        print(f)
    print('=======folders only in dir2=======')
    for f in dir2_only:
        print(f)
    print('=======files only in dir1=======')
    for f in file1_only:
        print(f)
    print('=======files only in dir2=======')
    for f in file2_only:
        print(f)

def diff_file(f1, f2):
    arr1=[]
    arr2=[]
    with open(f1, 'r') as f:
        arr1 = f.readlines()
    with open(f2, 'r') as f:
        arr2 = f.readlines()
    f1_only = set(arr1) - set(arr2)
    f2_only = set(arr2) - set(arr1)
    print ('----lines only in file1----')
    print(f1_only)
    print ('----lines only in file2----')
    print(f2_only)

if __name__ == "__main__":
    #diff_folder("1\\1-1", "1\\1-2")
    diff_file('1\\1-1\\test.txt', '1\\1-2\\test.txt')