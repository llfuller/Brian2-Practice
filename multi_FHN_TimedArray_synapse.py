# Same as 1_FHN_TimedArray.py, except it contains synaptic connections
from brian2 import *
import scipy as sp
n = 9
duration = 0.3 * second
num_samples = int(duration/defaultclock.dt) # 10,000 samples
tau = 10*ms # time constant
# Time-variable external current:
t_recorded = arange(num_samples)*defaultclock.dt
A=10
B=0
f=10/ms
# Linear Current
# dvdtExt_recorded = TimedArray(A*t_recorded*mV/(ms*ms)/1000, dt=defaultclock.dt)
# Current Steps
# dvdtExt_recorded = TimedArray(A*t_recorded*mV/(ms*ms)/1000//0.1*0.1, dt=defaultclock.dt)
# Sinusoidal Current
dvdtExt_recorded = TimedArray(A*cos(B*t_recorded/ms)*(mV/ms), dt=defaultclock.dt)

print(len(t_recorded))
print(dvdtExt_recorded.values)

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
dv/dt = v/ms - v**3 /(3*mV*mV*ms) - w/ms + dvdtExt - z*(v-nu)/ms : volt
dw/dt = (v + a - b*w)/tau : volt 
dz/dt = gSum*G/ms - z/ms : 1
nu = -1.5*mV : volt
v0 : volt
a = 0*mV : volt
b = 0 : 1
dvdtExt = dvdtExt_recorded(t) : volt/second
G = (v>0*mV) : 1
gSum : 1
'''

group = NeuronGroup(n, eqs, threshold = 'v > 2*mV', reset = 'v = 0*mV', refractory = 5*ms, method = "rk4")
#initial conditions:
group.v = 0*mV
group.w = 0*mV
# Assign different v0 to each neuron:
# group.v0 = '5*(i+1)*mV' #use for 3 neurons
group.v0 = '1.0/100*mV'

# #Synapses (useless for adding inhibition? My inhibitory equations need to apply outside of just neuron firings...
# S = Synapses(group, group, on_pre = "v += 0.2*mV")
# S.connect(condition = 'i!=j')


@network_operation(dt=defaultclock.dt) # worry: does this lag a frame behind? # Also see documentation pg124
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


monitor = SpikeMonitor(group)
M = StateMonitor(group, variables=True, record=True)
run(duration)


figure()
# Plot current
plot(M.t/ms, M.dvdtExt[0]*(n/10)/amp, 'y')

# plot(M.t/ms, M.G[0]*(n/10)/amp, 'y')

# Plot raster of neurons spikes
for j in range(1,n):
    plot(monitor.t/ms, monitor.i, '.k')
xlabel('spike time (ms)')
ylabel('neuron index')
show()

# # Plot current vs time of neurons
print("Length of M: "+str(len(M)))
print(M)
for i in range(1,n):
    plot(M.t / ms, M[i].v / mV, label="V"+str(i))
# # plot(M.t/ms, M[0].v / mV, color="k")
# # plot(M.t/ms, M[1].v / mV)
# # plot(M.t/ms, M[2].v / mV, color="r")
xlabel('time (ms)')
ylabel('voltage (mV)')
legend()
# plot(t_recorded, dvdtExt_recorded)
show()