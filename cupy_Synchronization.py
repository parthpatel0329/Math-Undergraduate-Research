import cupy as np
import numpy
from matplotlib import pyplot as plt
from matplotlib import animation

def nw_initial_sample(n,line,number):
    thesample = np.ones(n+3) * (-np.inf)
    for i in range(1,line+2):
        thesample[i] = number
    return thesample

def nw_normal_initial_sample(n,line,number):
    thesample = np.ones(n+3) * (-np.inf)
    x = 0
    y = line
    for i in range(1,line+2):
        np.random.seed(i)
        thesample[i] = number + np.random.normal(0,np.absolute(x-y) ** (1/3))
        x += 1
        y -= 1
    return thesample

def iter_step(current_sample,current_normal,r):
    w = np.random.exponential(1, r+3)
    
    tmp = current_sample[0:r+3]
    current_sample[0:r+3] = np.maximum(np.roll(tmp, 1), tmp) + w
    
    tmp = current_normal[0:r+3]
    current_normal[0:r+3] = np.maximum(np.roll(tmp, 1), tmp) + w
    
    return current_sample, current_normal

def sample(n, initial_condition, initial_normal, line):
    current_condition = initial_condition
    current_normal = initial_normal
    num = int((line+3)/2)
    cordsSample.append(current_condition[num-100:num+100+1]-current_condition[num])
    cordsNormal.append(current_normal[num-100:num+100+1]-current_normal[num])
    for i in range(line+1,n+1):
        print(i)
        current_condition, current_normal = iter_step(current_condition,current_normal,i)
        if i % 2 == 0:
            num = int((i+3)/2)
            cordsSample.append(current_condition[num-100:num+100+1]-current_condition[num])
            cordsNormal.append(current_normal[num-100:num+100+1]-current_normal[num])
    return 'Done'

cordsSample = []
cordsNormal = []
n = 300402
#setting line = 6 and number = 3 means that [(0,6),(1,5),(2,4),(3,3),(4,2),(5,1),(6,0)] will all be set to 3.
line = 200402
number = 0
print(sample(n,nw_initial_sample(n * 2,line,number),nw_normal_initial_sample(n * 2,line,number),line))

plt.rc('figure', figsize=(10, 10))

fig,ax=plt.subplots(1,1)

def animate(i):
    ax.cla()
    ax.set_title('LPP')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim([-5,205])
    ax.set_ylim([-100,100])
    ax.plot(np.asnumpy(cordsSample[i]),color='red',label="h(0,x)=0")
    ax.plot(np.asnumpy(cordsNormal[i]),color='blue',label="h(0,x)=indep. N(0,|x|^1/3)")
    ax.legend(frameon=False, fancybox=True, framealpha=0.5)

writervideo = animation.FFMpegWriter(fps=24)
anim = animation.FuncAnimation(fig, animate, numpy.arange(0, len(cordsSample), 1), interval=200)
anim.save('maximum.mp4', writer=writervideo)