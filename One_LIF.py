# Manual practice replicating IF_curve_LIF.py originally written by Brian2 team.
# Small changes (plotted voltage vs time here) made

from brian2 import *

n = 1
duration = 0.1 * second
tau = 10*ms
dvdtExt = 0.0*mV/ms  # Every 0.1 mV/ms pushes effective v0 threshold for spiking down by 1 mV
eqs = '''
dv/dt = dvdtExt + (v0-v)/tau : volt (unless refractory)
Iext : amp
v0 : volt
'''
group = NeuronGroup(n, eqs, threshold = 'v > 10*mV', reset = 'v = 0*mV', refractory = 5*ms)
#initial voltage:
group.v = 0*mV
# Neuron asymptotically approaches this over time
group.v0 = 20*mV

monitor = SpikeMonitor(group)
stateMon = StateMonitor(group, variables=True, record=True)

run(duration)

plot(stateMon.t/ms, stateMon[0].v / mV)
xlabel('t (ms)')
ylabel('Voltage (mV)')
show()