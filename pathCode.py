import numpy as np
from joblib import Parallel, delayed
    
def nw_initial_sample(n):
    thesample = np.ones(n + 3) * (-np.inf)
    thesample[1] = 0
    return thesample

def cords(n,x,y,track):
    cord1 = [x, y]
    cord2 = [y, x]
    ind1 = x+1
    ind2 = y+1
    for r in range(x+y, 0, -1):
        if track[r][ind1]:
            cord1[1] -= 1
        else:
            cord1[0] -= 1
            ind1 -= 1
        if track[r][ind2]:
            cord2[1] -= 1
        else:
            cord2[0] -= 1
            ind2 -= 1
        if (cord1[0] == cord2[0]) and (cord1[1] == cord2[1]):
            return (n-cord1[0],n-cord1[1])
    return None
    
def sample(n, file):
    c_zero = nw_initial_sample(n)
    track_zero = np.zeros((n+1, n+3))
    tmp1 = None
    tmp2 = None
    for r in range(1,n+1):
        w = np.random.exponential(1, r+3)
        a = c_zero[0:r+3]
        b = np.roll(a, 1)
        c = np.stack((b, a),axis=1)
        c_zero[0:r+3] = np.maximum(b,a) + w
        ind = np.argmax(c,axis=1)
        track_zero[r, 0:r + 3] += ind
        if r == 19999:
            tmp1 = c_zero[10000]
            tmp2 = c_zero[10001]
    if track_zero[20000][10001]:
        file.write('input cord: ' + str((0,1)) + '\n')
    else:
        file.write('input cord: ' + str((1,0)) + '\n')
    file.write('t = 19,999 cord point: ' + str(cords(10000,9999,10000,track_zero)) + '\n')
    file.write('t = 20,000 cord point: ' + str(cords(10000,9999,10001,track_zero)) + '\n')
    file.write('G(10000, 10000)-G(9999, 10000): ' + str(c_zero[10001]-tmp1) + '\n')
    file.write('G(10000, 10000)-G(10000, 9999): ' + str(c_zero[10001]-tmp2) + '\n')
    file.write('G(10000, 10000)-G(9999, 10001): ' + str(c_zero[10001]-c_zero[10000]) + '\n')
    file.write('G(10000, 10000)-G(10001, 9999): ' + str(c_zero[10001]-c_zero[10002]) + '\n\n')
    return

def f(fileName):
    file = open(fileName, "a", buffering=1)
    num_samples = 100000
    n = 20000
    for _ in range(num_samples):
        sample(n, file)
    file.close()

fileNum = 64
files = ['data'+str(i)+'.txt' for i in range(1,fileNum+1)]
Parallel(n_jobs=fileNum)(delayed(f)(fileName) for fileName in files)
