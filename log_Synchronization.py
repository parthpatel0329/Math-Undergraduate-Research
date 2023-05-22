import cupy as np
import numpy
from matplotlib import pyplot as plt
from matplotlib import animation

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
    c_imj[0:r+3] = np.logaddexp(np.roll(tmp, 1), tmp) + w
    
    tmp = c_jmi[0:r+3]
    c_jmi[0:r+3] = np.logaddexp(np.roll(tmp, 1), tmp) + w
    
    tmp = c_abs[0:r+3]
    c_abs[0:r+3] = np.logaddexp(np.roll(tmp, 1), tmp) + w
    
    return c_imj, c_jmi, c_abs

def sample(n, i_imj, i_jmi, i_abs, line):
    c_imj = i_imj
    c_jmi = i_jmi
    c_abs = i_abs
    num = int((line+3)/2)
    cordsIMJ.append(c_imj[num-100:num+100+1]-c_imj[num])
    cordsJMI.append(c_jmi[num-100:num+100+1]-c_jmi[num])
    cordsABS.append(c_abs[num-100:num+100+1]-c_abs[num])
    for i in range(line+1,n+1):
        print(i)
        c_imj, c_jmi, c_abs = iter_step(c_imj, c_jmi, c_abs,i)
        if i % 2 == 0:
            num = int((i+3)/2)
            cordsIMJ.append(c_imj[num-100:num+100+1]-c_imj[num])
            cordsJMI.append(c_jmi[num-100:num+100+1]-c_jmi[num])
            cordsABS.append(c_abs[num-100:num+100+1]-c_abs[num])
    return 'Done'

cordsIMJ = []
cordsJMI = []
cordsABS = []
n = 400402
line = 200402
s_imj = nw_initial_sample_i_minus_j(n * 2,line)
s_jmi = nw_initial_sample_j_minus_i(n * 2,line)
s_abs = nw_initial_sample_abs_i_minus_j(n * 2,line)
print(sample(n,s_imj,s_jmi,s_abs,line))

plt.rc('figure', figsize=(10, 10))

fig,ax=plt.subplots(1,1)

def animate(i):
    ax.cla()
    ax.set_title('DPRE')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim([-5,205])
    ax.set_ylim([-200,200])
    ax.plot(np.asnumpy(cordsIMJ[i]),color='r',label="f(i,j)=i-j")
    ax.plot(np.asnumpy(cordsJMI[i]),color='b',label="f(i,j)=j-i")
    ax.plot(np.asnumpy(cordsABS[i]),color='k',label="f(i,j)=|i-j|")
    ax.legend(frameon=False, loc=2)

writervideo = animation.FFMpegWriter(fps=24)
anim = animation.FuncAnimation(fig, animate, numpy.arange(0, len(cordsABS), 1), interval=200)
anim.save('logaddexp.mp4', writer=writervideo)