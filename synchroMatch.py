import cupy as np

def nw_initial_sample_i_minus_j(n,line):
    thesample = np.ones(n+3) * (-np.inf)
    i = 0
    j = line
    for ind in range(1,line+2):
        thesample[ind] = i - j
        i += 1
        j -= 1
    return thesample

def nw_initial_sample_j_minus_i(n,line):
    thesample = np.ones(n+3) * (-np.inf)
    i = 0
    j = line
    for ind in range(1,line+2):
        thesample[ind] = j - i
        i += 1
        j -= 1
    return thesample

def nw_initial_sample_abs_i_minus_j(n,line):
    thesample = np.ones(n+3) * (-np.inf)
    i = 0
    j = line
    for ind in range(1,line+2):
        thesample[ind] = abs(i - j)
        i += 1
        j -= 1
    return thesample

def iter_step(c_imj, c_jmi, c_abs, r):
    w = np.random.normal(0, 1, r+3)
    
    tmp = c_imj[0:r+3]
    c_imj[0:r+3] = np.maximum(np.roll(tmp, 1), tmp) + w
    
    tmp = c_jmi[0:r+3]
    c_jmi[0:r+3] = np.maximum(np.roll(tmp, 1), tmp) + w
    
    tmp = c_abs[0:r+3]
    c_abs[0:r+3] = np.maximum(np.roll(tmp, 1), tmp) + w
    
    return c_imj, c_jmi, c_abs

def sample(n, i_imj, i_jmi, i_abs, line):
    c_imj = i_imj
    c_jmi = i_jmi
    c_abs = i_abs
    num = int((line+3)/2)
    cordsIMJ = c_imj[num-50:num+50+1]-c_imj[num]
    cordsJMI = c_jmi[num-50:num+50+1]-c_jmi[num]
    cordsABS = c_abs[num-50:num+50+1]-c_abs[num]
    if np.array_equal(cordsABS, cordsIMJ):
        print(line,'equal','imj')
    elif np.isclose(cordsABS, cordsIMJ, rtol=1e-1, atol=1e-1).sum() == 101:
        print(line,'close','imj')
    if np.array_equal(cordsABS, cordsJMI):
        print(line,'equal','jmi')
    elif np.isclose(cordsABS, cordsJMI, rtol=1e-1, atol=1e-1).sum() == 101:
        print(line,'close','jmi')
    for i in range(line+1,n+1):
        c_imj, c_jmi, c_abs = iter_step(c_imj, c_jmi, c_abs,i)
        if i % 2 == 0:
            num = int((i+3)/2)
            cordsIMJ = c_imj[num-50:num+50+1]-c_imj[num]
            cordsJMI = c_jmi[num-50:num+50+1]-c_jmi[num]
            cordsABS = c_abs[num-50:num+50+1]-c_abs[num]
            
            if np.array_equal(cordsABS, cordsIMJ):
                print(i,'equal','imj')
            elif np.isclose(cordsABS, cordsIMJ, rtol=1e-1, atol=1e-1).sum() == 101:
                print(i,'close','imj')
            if np.array_equal(cordsABS, cordsJMI):
                print(i,'equal','jmi')
            elif np.isclose(cordsABS, cordsJMI, rtol=1e-1, atol=1e-1).sum() == 101:
                print(i,'close','jmi')
        
    return 'Done'

n = 2000000
line = 200402
s_imj = nw_initial_sample_i_minus_j(n * 2,line)
s_jmi = nw_initial_sample_j_minus_i(n * 2,line)
s_abs = nw_initial_sample_abs_i_minus_j(n * 2,line)
print(sample(n,s_imj,s_jmi,s_abs,line))