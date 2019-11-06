# Same as 1000_LIF_TimedArray.py, except it contains synaptic connections
from brian2 import *
n = 1000
duration = 0.3 * second
num_samples = int(duration/defaultclock.dt) # 10,000 samples
tau = 10*ms
# Time-variable external current:
maxNumClockTicks = int(1.0*ms/defaultclock.dt) # 10
t_recorded = arange(num_samples)*defaultclock.dt
A=1
f=10/ms
# Linear Current
# dvdtExt_recorded = TimedArray(A*t_recorded*mV/(ms*ms)/1000, dt=defaultclock.dt)
# Current Steps
# dvdtExt_recorded = TimedArray(A*t_recorded*mV/(ms*ms)/1000//0.1*0.1, dt=defaultclock.dt)
# Sinusoidal Current
dvdtExt_recorded = TimedArray(sin(A*t_recorded/ms)*(mV/ms), dt=defaultclock.dt)

print(len(t_recorded)) # 10,000 elements
print(dvdtExt_recorded.values)
eqs = '''
dv/dt = dvdtExt + (v0-v)/tau : volt (unless refractory)
v0 : volt
dvdtExt = dvdtExt_recorded(t) : volt/second
'''
group = NeuronGroup(n, eqs, threshold = 'v > 10*mV', reset = 'v = 0*mV', refractory = 5*ms)
#initial voltage:
group.v = 0*mV
# Assign different v0 to each neuron:
# group.v0 = '5*(i+1)*mV' #use for 3 neurons
group.v0 = '(i+1)/100*mV'

deltaV = 2*mV
S = Synapses(group, group, on_pre = "v += deltaV")
S.connect(condition = 'i!=j')


monitor = SpikeMonitor(group)
M = StateMonitor(group, variables=True, record=True)
run(duration)


figure()
# Plot current
plot(M.t/ms, M.dvdtExt[0]*(n/10)/amp, 'y')
# Plot raster of neurons spikes
plot(monitor.t/ms, monitor.i, '.k')

# Plot current vs time of neurons
# plot(M.t/ms, M[0].v / mV, color="k")
# plot(M.t/ms, M[1].v / mV)
# plot(M.t/ms, M[2].v / mV, color="r")
#

# plot(t_recorded, dvdtExt_recorded)
xlabel('spike time (ms)')
ylabel('neuron index')
show()