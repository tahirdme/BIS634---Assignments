import time 
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing 
import math 

def alg2(data):
    if len(data) <= 1:
        return data
    else:
        split = len(data) // 2
        left = iter(alg2(data[:split])) # left data
        right = iter(alg2(data[split:])) # right data
        result = []
    # note: this takes the top items off the left and right piles
        left_top = next(left)
        right_top = next(right)
    # combining the left and right data
    while True:
        if left_top < right_top:
            result.append(left_top)
            try:
                left_top = next(left)
            except StopIteration:
            # nothing remains on the left; add the right + return
                return result + [right_top] + list(right)
        else:
            result.append(right_top)
            try:
                right_top = next(right)
            except StopIteration:
        # nothing remains on the right; add the left + return
                return result + [left_top] + list(left)
                
                
def data1(n, sigma=10, rho=28, beta=8/3, dt=0.01, x=1, y=1, z=1):
    import numpy
    state = numpy.array([x, y, z], dtype=float)
    result = []
    for _ in range(n):
        x, y, z = state
        state += dt * numpy.array([
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z
        ])
        result.append(float(state[0] + 30))
    return result


def alg2_parallel(data):
    if len(data) <= 1:
        return data
        
    else:
        split = len(data) // 2
        with multiprocessing.Pool() as m:   
            [left, right] = m.map(alg2, [data[:split], data[split:]])
            
        left = iter(left)
        right = iter(right)
        # combining the left and right data
        result = []
        left_top = next(left)
        right_top = next(right)
        
    while True:
        if left_top < right_top:
            result.append(left_top)
            try:
                left_top = next(left)
            except StopIteration:
            # nothing remains on the left; add the right + return
                return result + [right_top] + list(right)
        else:
            result.append(right_top)
            try:
                right_top = next(right)
            except StopIteration:
        # nothing remains on the right; add the left + return
                return result + [left_top] + list(left)



if __name__ == '__main__':

    #n = 20000   
    n = 2**23
    data_in = data1(n)

    t_start_1 = time.perf_counter()
    alg2_parallel(data_in)     
    t_end_1 = time.perf_counter()

    time_parallel= t_end_1 - t_start_1


    t_start_2 = time.perf_counter()
    alg2(data_in)    
    t_end_2 = time.perf_counter()     

    time_alg2 = t_end_2 - t_start_2


    print(time_parallel,  time_alg2)

   