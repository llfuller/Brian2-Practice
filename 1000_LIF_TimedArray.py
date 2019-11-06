from brian2 import *

n = 10000
duration = 1.0 * second
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
group.v0 = '20*mV * i / (n-1)' # crashes if n=1

monitor = SpikeMonitor(group)

M = StateMonitor(group, variables=True, record=True)

run(duration)

figure()
#Plot current
plot(M.t/ms, M.dvdtExt[0]*(n/10)/amp, 'y')
#Plot raster of neurons spikes
plot(monitor.t/ms, monitor.i, '.k')

# plot(t_recorded, dvdtExt_recorded)

xlabel('spike time (ms)')
ylabel('neuron index')
show()