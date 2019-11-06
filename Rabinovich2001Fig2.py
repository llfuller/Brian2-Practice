# Attempt at recreating Rabinovich 2001 paper figure 2.
from brian2 import *
import scipy as sp
n = 9
duration = 50000*ms
num_samples = int(duration/defaultclock.dt) # 10,000 samples
# Time-variable external current:
t_recorded = arange(num_samples)*defaultclock.dt
A=0.1
B=0
f=10/ms
# S is 'stimulus'
# Linear Current
# S_recorded = TimedArray(A*t_recorded/(ms)/1000, dt=defaultclock.dt) # ms term cancels units of t_recorded
# Current Steps
# S_recorded = TimedArray(A*t_recorded/(ms)/1000//0.1*0.1, dt=defaultclock.dt)
# Sinusoidal Current
S_recorded = TimedArray(A*cos(B*t_recorded/ms), dt=defaultclock.dt)
GivenS = [0.1,.15,0,0,.15,0.1,0,0,0]

print(len(t_recorded))
print(S_recorded.values)

# Inhibitory max amplitude
g = zeros((n,n)) #needs to be +1,+1 larger than usual (extra row and column) to make the following clean:
# Inhibitory pairs: (presynaptic, postsynaptic):
inhibPairs = [[1,5],[5,2],[2,1],[2,4],[4,5],[5,2],
              [6,5],[2,6],[3,6],[5,3],[7,4],[5,7],
              [8,4],[5,8],[8,6],[8,9],[9,5]]
for pair in inhibPairs:
    # The -1 corrects for computer index starting at zero vs. neurons starting at 1.
    g[pair[0]-1,pair[1]-1] = 2

eqs = '''
dv/dt = (v - v**3 /(3) - w - z*(v-nu) + 0.35 + S)/tau1: 1
dw/dt = (v - b*w + a)/second : 1 
dz/dt = (gSum*G - z)/tau2 : 1
tau1 = 0.08 *ms : second # Could be wrong. I don't know if it should be in ms
tau2 = 3.1 *ms  : second
a = 0.7 : 1
b = 0.8 : 1
nu = -1.5 : 1
S : 1
# S = S_recorded(t) : 1
G = (v>0) : 1
gSum : 1
'''

group = NeuronGroup(n, eqs, threshold = 'v > 1.2', method = "rk4")
#initial conditions:
group.v = -1.2
group.w = -0.62
group.z = 0
group.S = GivenS

# #Synapses (useless for adding inhibition? My inhibitory equations need to apply outside of just neuron firings...
# S = Synapses(group, group, on_pre = "v += 0.2*mV")
# S.connect(condition = 'i!=j')


@network_operation(dt=defaultclock.dt) # worry: does this lag a frame behind? Also (separately) see documentation pg124
def inhibition():
    # for i in range(1,n):
    #     sum = 0.0
    #     for j in range(1,n):
    #         if i!=j:
    #             multiple = g[j,i]*group.G[j]
    #             sum += multiple
    #     group.gSum[i] = sum
    # The above for loop describes what the following assignment does
    group.gSum.set_item(slice(None), sp.dot(sp.transpose(g), sp.array(group.G.__array__())))
    # pass


monitor = SpikeMonitor(group)
M = StateMonitor(group, variables=True, record=True)
run(duration)

# figure()
# plot(M.t/ms, M.S[0]*(n/10), 'y')

# Plot current
# plot(M.t/ms, M.G[0]*(n/10)/amp, 'y')

# Plot raster of neurons spikes
for j in range(0,n):
    plot(monitor.t/ms, monitor.i, '.k')
xlabel('spike time (ms)')
ylabel('neuron index')
show()

# print("Length of M: "+str(len(M)))
# print(M)

# Plot v(t) of neurons
fig, axs = plt.subplots(n)
fig.suptitle('V(t) [maybe] over time')
for i in range(0,n):
    axs[i].plot(M.t / ms, M[i].v)
    axs[i].set(ylabel = "V"+str(i+1))
axs[n-1].set(xlabel = 'time (ms)')
# # plot(M.t/ms, M[0].v / mV, color="k")
# # plot(M.t/ms, M[1].v / mV)
# # plot(M.t/ms, M[2].v / mV, color="r")
# plot(t_recorded, S_recorded)
show()