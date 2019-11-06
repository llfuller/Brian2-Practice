from brian2 import *

n = 1000
duration = 1 * second
num_samples = int(duration/defaultclock.dt) # 10,000 samples

tau = 10*ms

# Time-variable external current:
dClockdt = defaultclock.dt # 100 microseconds
t_recorded = arange(num_samples)*defaultclock.dt # series of maxNumClockTicks from 0 to (numSamples-1)*defaultClock.dt
A=1
f=10/ms
dvdtExt_recorded = TimedArray(A*(f*t_recorded) * mV/ms, dt=defaultclock.dt)

print(num_samples)
print(t_recorded)
print(dvdtExt_recorded.values)