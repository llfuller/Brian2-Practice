# Manual practice replicating IF_curve_LIF.py originally written by Brian2 team.
# Small changes (plotted variables and added input current) made
# Same as One_LIF.py, but uses 1000 neurons.

from brian2 import *

n = 1000
duration = 1 * second
tau = 10*ms
dvdtExt = 1.0*mV/ms  # Every 0.1 mV/ms pushes effective v0 threshold for spiking down by 1 mV
eqs = '''
dv/dt = dvdtExt + (v0-v)/tau : volt (unless refractory)
Iext : amp
v0 : volt
'''
group = NeuronGroup(n, eqs, threshold = 'v > 10*mV', reset = 'v = 0*mV', refractory = 5*ms)
#initial voltage:
group.v = 0*mV
# Assign different v0 to each neuron:
group.v0 = '20*mV * i / (n-1)' # crashes if n=1

monitor = SpikeMonitor(group)


run(duration)

plot(monitor.t/ms, monitor.i, '.k')
xlabel('spike time (ms)')
ylabel('neuron index')
show()