import time

"""
# run this command in the terminal
# When you need more than manual timers:    
# python -m cProfile -s cumtime cp_test.py 

Output :

finished sleeping for 5 seconds
finished sleeping for 3 seconds
finished sleeping for 1 second
         12 function calls in 9.009 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    9.009    9.009 {built-in method builtins.exec}
        1    0.000    0.000    9.009    9.009 cp_test.py:1(<module>)
        3    9.008    3.003    9.008    3.003 {built-in method time.sleep}
        1    0.000    0.000    5.003    5.003 cp_test.py:3(sleep_for_5_seconds)
        1    0.000    0.000    3.001    3.001 cp_test.py:7(sleep_for_3_seconds)
        1    0.000    0.000    1.005    1.005 cp_test.py:11(sleep_for_1_second)
        3    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

This shows every function call sorted by cumulative time. For line-by-line profiling:
meaning 
1. sleep_for_5_seconds 5.003 seconds total
2. sleep_for_3_seconds 3.001 seconds total
3. sleep_for_1_second 1.005 seconds total


"""

def sleep_for_5_seconds():
    time.sleep(5)
    print("finished sleeping for 5 seconds")

def sleep_for_3_seconds():
    time.sleep(3)
    print("finished sleeping for 3 seconds")

def sleep_for_1_second():
    time.sleep(1)
    print("finished sleeping for 1 second")


if __name__ == "__main__":
    sleep_for_5_seconds()
    sleep_for_3_seconds()
    sleep_for_1_second()
