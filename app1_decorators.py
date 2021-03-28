"""
    decorators 
    fullTraceBackDecorator . usage . \@logFullTraceback 
    maxRetryDecorator . usage \@maxRetry(5) 
    timeFunc. usage \@timeFunc
"""

import traceback 
import time 
import random

def logtraceback(func):
    def wrap(*args, **kwarg):
        try:
            func(*args, **kwarg)
        except Exception :
            print(traceback.format_exc())
    return wrap

@logtraceback
def test_trace():
    a=1
    b=0
    c=a/b




def retry(times=5):
    def wrap(func):
        def inner(*arg, **kwarg):
            count = 0
            while count < times:
                try:
                    func(*arg, **kwarg)
                    print('Done')
                except Exception:
                    print(f'retrying {count}/{times} in 1 sec')
                    count+=1
                    time.sleep(1)
        return inner 
    return wrap 

@retry(10)
def test_retry():
    while True :
        raise Exception ("test")


def timefunc(func):
    def wrap(*arg, **kwarg):
        start = time.time()
        func(*arg, **kwarg)
        end = time.time()
        print(f'done .took {end-start}second')
    return wrap

@timefunc
def test_time():
    time.sleep(random.randint(1,5000)/1000)


if __name__ == "__main__":
    test_trace()
    #test_retry()
    #test_time()
    