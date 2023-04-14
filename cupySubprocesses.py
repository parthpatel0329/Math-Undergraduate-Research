import cupy as np
import numpy
from joblib import Parallel, delayed
import os
import time

def nw_initial_sample(t_end, t_start, initial_condition):
    thesample = np.ones(t_end + 3) * (-np.inf)
    thesample[1:t_start + 2] = initial_condition
    return thesample

def iter_step(current_sample, t):
    tmp = current_sample[0:t + 3]
    current_sample[0:t + 3] = np.logaddexp(np.roll(tmp, 1), tmp) + np.random.normal(0, 1, t + 3)
    current_sample[0] = -np.inf
    current_sample[t+2] = -np.inf
    return current_sample

def sample(t_end, initial_condition, t_start, k):
    current_condition = initial_condition
    for t in range(t_start + 1, t_end + 1):
        current_condition = iter_step(current_condition, t)
    mid = int((t_end+3)/2)
    line = current_condition[mid-k:mid+k+1]
    return line

def f(fileName):
    
    '''Change the options below:'''

    t_start = 0
    t_end = 100000
    k = 500

    '''
    Possible Initial Conditions:

    Normal:
    mu, sigma = 0, 1
    initial_condition = np.random.normal(mu, sigma, t_start + 1)

    Exponential:
    initial_condition = np.random.exponential(1, t_start + 1)

    Zeros:
    initial_condition = 0
    '''
    initial_condition = 0

    #number of samples you want
    n_samples = 3

    '''~~~~~~~~~~~~~~~~~~~~~~~~~'''

    file = open(fileName, "a")
    for n in range(n_samples):
        samp = sample(t_end, nw_initial_sample(t_end, t_start, initial_condition), t_start, k)
        #cupy with savetxt isn't working for some reason so use numpy instead
        numpy.savetxt(file, np.asnumpy(samp), newline=" ")
        #np.savetxt(file, samp, newline=" ")
        file.write('\n')
    file.close()
    
#fileNum is how many processes you want, default is the count of the number of CPUs in your system
start_time = time.time()
fileNum = 10
files = ['samp'+str(i)+'.txt' for i in range(1,fileNum+1)]
Parallel(n_jobs=fileNum)(delayed(f)(fileName) for fileName in files)
print("--- %s seconds ---" % (time.time() - start_time))