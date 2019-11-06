# Most likely entirely an example taken from Brian2 website or tutorial.
from brian2 import *
A = 2.5
f = 10*Hz
tau = 5*ms
# Let's create an array that couldn't be
# reproduced with a formula
num_samples = int(200*ms/defaultclock.dt)
print("Number of samples: "+str(num_samples))
I_arr = zeros(num_samples)
#Making currents a random number for spans of 100 indices with random starting indices
for _ in range(100):
    a = randint(num_samples)
    print("a = " +str(a))
    I_arr[a:a+100] = rand()

I_recorded = TimedArray(A*I_arr, dt=defaultclock.dt)
eqs = '''
dv/dt = (I-v)/tau : 1
I = I_recorded(t) : 1
'''
G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
M = StateMonitor(G, variables=True, record=True)
run(200*ms)
plot(M.t/ms, M.v[0], label='v')
plot(M.t/ms, M.I[0], label='I')
xlabel('Time (ms)')
ylabel('v')
legend(loc='best');
show()