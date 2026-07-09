from memory_profiler import profile
"""
python -m memory_profiler memory_profiling_01.py 
Filename: memory_profiling_01.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     3     23.1 MiB     23.1 MiB           1   @profile
     4                                         def my_func():
     5     30.7 MiB      7.6 MiB           1       a = [1] * (10**6)
     6    183.3 MiB    152.6 MiB           1       b = [2] * (2 * 10**7)
     7     30.7 MiB   -152.6 MiB           1       del b
     8     30.7 MiB      0.0 MiB           1       return a


Filename: memory_profiling_01.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    10     30.7 MiB     30.7 MiB           1   @profile
    11                                         def my_func_2():
    12     30.7 MiB      0.0 MiB           1       a = [1] * (10**6)
    13    183.3 MiB    152.6 MiB           1       b = [2] * (2 * 10**7)
    14     30.7 MiB   -152.6 MiB           1       del b
    15     30.7 MiB      0.0 MiB           1       return a

"""
@profile
def my_func():
    a = [1] * (10**6)
    b = [2] * (2 * 10**7)
    del b
    return a

@profile
def my_func_2():
    a = [1] * (10**6)
    b = [2] * (2 * 10**7)
    del b
    return a

if __name__ == '__main__':
    my_func()
    my_func_2()
