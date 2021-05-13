"""
find 5 biggest files in folder and sub folders 
"""
import os 
import heapq
import time 

def top_large_files(dir, top = 5):
    start = time.time()
    count = 0
    if not os.path.isdir(dir):
        print('Must be a folder path')
        return 

    res = []
    for root, _, files in os.walk(dir):
        for f in files:
            p = os.path.join(root, f)
            heapq.heappush(res, (os.path.getsize(p), p))
            if len(res) > top:
                heapq.heappop(res)
            count+=1
            #print(f'{count}files scanned')
    end = time.time()
    print(f'Top{top} largest size(in bytes) files: {res}')
    print(f'Took {end-start} seconds')
    return res 

# TODO Speed up the process use multi-processing and merge result 

if __name__ == "__main__":
    top_large_files("C:\\Program Files (x86)") 
    