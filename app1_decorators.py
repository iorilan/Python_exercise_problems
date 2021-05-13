"""
    decorators 
    fullTraceBackDecorator . usage . \@logFullTraceback 
    maxRetryDecorator . usage \@maxRetry(5) 
    timeFunc. usage \@timeFunc
"""

import traceback 
import time 
import random
from functools import wraps

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


class retry_class:
    """
        using wraps
    """
    def __init__(self, times=5):
        self.times=times
    
    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            count = 0
            while count < self.times:
                try:
                    print(args)
                    print(kwargs)
                    func(*args, **kwargs)
                    print('Done')
                except Exception:
                    print(f'retrying {count}/{self.times} in 1 sec')
                    count+=1
                    time.sleep(1)
        return inner 
    

def retry(times=5):
    def wraper(func):
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
    return wraper

#@retry(10)
@retry_class(5)
def test_retry(a=1, b=2):
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
    #test_trace()
    test_retry()
    #test_time()
    