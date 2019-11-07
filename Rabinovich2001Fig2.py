# Attempt at recreating Rabinovich 2001 paper figure 2.
from brian2 import *
import scipy as sp
# print(defaultclock.dt)
defaultclock.dt = 0.05*ms # Half the usual timestep
n = 9
duration = 200*ms # at and after 141ms, this breaks for neurons 4 and 6. Those neurons explode afterward

def Modulation(t):
    return (t<100*ms) # Reverse Heaviside Step

# Time-varying input current section
num_samples = int(duration/defaultclock.dt) # 10,000 samples
# Time-variable external current:
t_recorded = arange(num_samples)*defaultclock.dt
A=0.5
f=2*pi/20.0/ms
# S is 'stimulus'
# Linear Current
# S_recorded = TimedArray(A*t_recorded/(ms)/1000, dt=defaultclock.dt) # ms term cancels units of t_recorded
# Current Steps
# S_recorded = TimedArray(A*t_recorded/(ms)/1000//0.1*0.1, dt=defaultclock.dt)
# Sinusoidal Current
S_recorded = TimedArray(A*cos(f*t_recorded)*Modulation(t_recorded), dt=defaultclock.dt)
# End of time-varying input current section
GivenS = [0.1,.15,0,0,.15,0.1,0,0,0]

print(len(t_recorded))
print(S_recorded.values)

# Inhibitory max amplitude
g = zeros((n,n)) #needs to be +1,+1 larger than usual (extra row and column) to make the following clean:
# Inhibitory pairs: (presynaptic, postsynaptic):
inhibPairs = [[1,5],[5,2],[2,1],[2,4],[4,5],
              [6,5],[2,6],[3,6],[5,3],[7,4],[5,7],
              [8,4],[5,8],[8,6],[8,9],[9,5]]
for pair in inhibPairs:
    # The -1 corrects for computer index starting at zero vs. neurons starting at 1.
    g[pair[0]-1,pair[1]-1] = 2

eqs = '''
dv/dt = (v - v**3 /(3) - w - z*(v-nu) + 0.35 + S)/tau1: 1
dw/dt = (v - b*w + a)/ms : 1 
dz/dt = (gSumG - z)/tau2 : 1
tau1 = 0.08 *ms : second 
tau2 = 3.1 *ms  : second
a = 0.7 : 1
b = 0.8 : 1
nu = -1.5 : 1
# S : 1
S = S_recorded(t) : 1
G = (v>0) : 1
gSumG : 1
'''

group = NeuronGroup(n, eqs, threshold = 'v > 1.2', method = "rk4")
#initial conditions:
group.v = -1.2
group.w = -0.62
group.z = 0
# group.S = GivenS

syn = Synapses(group, group, model = 'gSumG_post = 2*(v_pre>0) : 1 (summed)')
syn.connect(i=[0,3,5,8], j=4)
syn.connect(i=1, j=[0,5])
syn.connect(i=2, j=5)
syn.connect(i=4, j=[1,2,6,7])
syn.connect(i=6, j=3)
syn.connect(i=7, j=[3,5,8])


monitor = SpikeMonitor(group)
M = StateMonitor(group, variables=True, record=True)
run(duration)

# Plot raster of neurons spikes
for j in range(0,n):
    plot(monitor.t/ms, monitor.i, '.k')
xlabel('spike time (ms)')
ylabel('neuron index')
show()

# Plot v(t) of neurons
fig, axs = plt.subplots(n+1)
fig.suptitle('V(t) [maybe] over time')
axs[0].set(xlabel = 'time (ms)')
for i in range(n-1,-1,-1):
    axs[i].plot(M.t / ms, M[i].v)
    axs[i].set(ylabel = "V"+str(i+1))
axs[n].plot(M.t/ms, [S_recorded(t) for t in t_recorded], 'c') # universal driving current
# axs[n].plot(M.t/ms, M.G[0]*(n/10)/amp, 'y') # current in neuron 0
show()

# Result: neurons 6 blows up sometime after 100ms and before 200ms