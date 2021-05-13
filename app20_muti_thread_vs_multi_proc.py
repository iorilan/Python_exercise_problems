"""
cpu task — check prime number from 1–20000 .
io task — generate 20k guid write into csv file1000 rows per file . clean up all files after finish
test execution time for single threaded , multi-threaded and multi-processing

Results 
--
Windows (4 Core i5)
[single thread cpu task ] total : 14.984469652175903 sec
[multi-thread cpu task ] total : 9.49857497215271 sec
[multi-process cpu task ] total : 6.357367992401123 sec
[single thread io task ] total : 9.06583833694458 sec
[multi-thread io task ] total : 10.542978048324585 sec
[multi-process io task ] total : 7.662624359130859 sec
--
Ubuntu 18.04 vm (2 Cores)
[single thread cpu task ] total : 9.855742931365967 sec
[multi-thread cpu task ] total : 4.477677345275879 sec
[multi-process cpu task ] total : 2.953005313873291 sec
[single thread io task ] total : 5.596938371658325 sec
[multi-thread io task ] total : 17.54924726486206 sec
[multi-process io task ] total : 3.260897636413574 sec

"""
import csv 
import uuid
import threading
import time 
import multiprocessing
import os 

def io_task(start, end):
    with open(f'{start}_{end}.csv', mode='w') as csv_file:
        for i in range(start, end):
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['value'])
            writer.writerow([uuid.uuid4()])
    os.remove(f'{start}_{end}.csv')

def is_prime(n):
    for i in range(2,n):
        if n % 2 == 0:
            return False 
    return True

def cpu_task(arr):
    for i in arr:
        is_prime(i)

def single_thread_cpu():
    start = time.time()
    total = 20000
    cpu_task([x for x in range(2,total)])
    end = time.time()
    print(f'[single thread cpu task ] total : {(end-start)} sec')

def single_thread_io():
    s = time.time()
    total = 500000
    io_task(0, total)
    e = time.time()
    print(f'[single thread io task ] total : {(e-s)} sec')

def proc_do_cpu_task():
    start = time.time()
    total = 20000
    proc_count = 5
    pool = multiprocessing.Pool(proc_count)
    parr = []
    for i in range(2, proc_count + 1):
        nums = [x for x in range(2,total) if x%i == 0]
        p = pool.apply_async(cpu_task, args=(nums,))
        parr.append(p)
    for p in parr:
        p.get()
    pool.close()
    pool.join()
    end = time.time()
    print(f'[process cpu task ] total : {(end-start)} sec')

def thread_do_cpu_task():
    start = time.time()
    total = 20000
    thread_count = 5
    tarr = []
    for i in range(2, thread_count+1):
        nums = [x for x in range(2,total) if x%i == 0]
        t = threading.Thread(target=cpu_task, args=(nums,))
        tarr.append(t)
        t.start()
    for t in tarr:
        t.join()
    end = time.time()
    print(f'[thread cpu task ] total : {(end-start)} sec')

def proc_do_io_task():
    s = time.time()
    total = 500000
    proc_count = 5
    pool = multiprocessing.Pool(proc_count)
    parr = []
    for i in range(0, total, 1000):
        start, end = i, i+1000
        p = pool.apply_async(io_task, args=(start, end,))
        parr.append(p)
    for p in parr:
        p.get()
    pool.close()
    pool.join()
    e = time.time()
    print(f'[process io task ] total : {(e-s)} sec')

def thread_do_io_task():
    s = time.time()
    total = 500000
    tarr = []
    for i in range(0, total, 1000):
        start, end = i, i+1000
        t = threading.Thread(target=io_task, args=(start, end,))
        tarr.append(t)
        t.start()
    for t in tarr:
        t.join()
    e = time.time()
    print(f'[thread io task ] total : {(e-s)} sec')

if __name__ == "__main__":
    single_thread_cpu()
    #single_thread_io()
    #thread_do_cpu_task()
    #proc_do_cpu_task()
    #thread_do_io_task()
    #proc_do_io_task()