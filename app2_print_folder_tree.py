"""
BFS walk folder files print tree structure . 
dir name
file name (size)
"""

import os 

def dir_tree(path, ):
    level=1
    dirs =[path]
    child = [(path, level)]
    while dirs :
        parent = dirs.pop()
        subdirs = os.listdir(parent)
        for d in subdirs:
            path=os.path.join(parent, d)
            if os.path.isdir(path):
                dirs.append(path)
            child.append((path, level))
        level += 1
    while child:
        path , level = child.pop(0)
        print('--'*level,end='')
        if os.path.isdir(path):
            print(f'[d]{path}')
        else:
            size = os.path.getsize(path)
            print(f'[f]{path}({size} bytes)')


    

if __name__ == "__main__":
    dir_tree('1')