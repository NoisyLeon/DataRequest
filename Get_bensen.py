import obspy
from obspy.clients.fdsn.client import Client
import matplotlib.pyplot as plt
import numpy as np

starttime   = obspy.core.utcdatetime.UTCDateTime('2001-01-01')
endtime     = obspy.core.utcdatetime.UTCDateTime('2008-01-01')
client=Client('IRIS')
cat = client.get_events(starttime=starttime, endtime=endtime, minmagnitude=6.5,
                        minlatitude=25., maxlatitude=40., minlongitude=65., maxlongitude=75., catalog='ISC', magnitudetype='MS')


i = 1
evlo = cat[i].origins[0].longitude; evla = cat[i].origins[0].latitude
otime   = cat[i].origins[0].time
stla    = 34.945910; stlo   = -106.457200
dist, az, baz=obspy.geodetics.gps2dist_azimuth(evla, evlo, stla, stlo) # distance is in m
t0 = 3600.*2.

print evlo, evla
print cat[i].event_descriptions[0]
print otime
print 'Mw = ',cat[1].magnitudes[0].mag
st = client.get_waveforms(network='IU', station='ANMO', location='00', channel='LHZ',
                            starttime=otime, endtime=otime+t0, attach_response=True)
pre_filt = (0.001, 0.005, 1, 100.0)
st.detrend()
st.remove_response(pre_filt=pre_filt, taper_fraction=0.1)
st.filter(type='bandpass', freqmin=0.01, freqmax=0.05, corners=4)

tr1=st[0].copy()
tr2=st[0].copy()
# one-bit
data1 = tr1.data
data1[data1>0.] = 1.
data1[data1<0.] = -1.
# running average
data2 = tr2.data
N = int(80./tr1.stats.delta/2)
data3 = np.zeros(data2.size)
data3[:N] = data2[:N]
data3[-N:] = data2[-N:]
for i in xrange(data2.size):
    if i < N:
        continue
    if i > data2.size - N-1: break
    W   = 0.
    for j in xrange(2*N+1):
        if i-N+j < 0: print 'ERROR'
        if i-N+j > data2.size: print 'ERROR'
        W += np.abs(data2[i-N+j])
    print i, data2.size
    data3[i] = data2[i]/W*(2*N+1)

# 
time  = np.arange(tr1.stats.npts) * tr1.stats.delta
fig = plt.figure()

ax = fig.add_subplot(311)
# fig, ax = plt.subplots(311)
plt.plot(time, data2, 'k', lw=2)
# plt.xlabel( 'Time (sec)', fontsize=30)
plt.xlim([1000, 7200])
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax = fig.add_subplot(312)
# fig, ax = plt.subplots(312)
plt.plot(time, data1, 'k', lw=2)
# plt.xlabel( 'Time (sec)', fontsize=30)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
plt.xlim([1000, 7200])
plt.ylim([-1.2, 1.2])
ax = fig.add_subplot(313)
# fig, ax = plt.subplots(313)
plt.plot(time, data3, 'k', lw=2)
plt.xlabel( 'Time (sec)', fontsize=30)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
plt.xlim([1000, 7200])
plt.show()

# plt.xlabel( 'Period (sec)', fontsize=30)
# plt.ylabel('Velocity (km/s)', fontsize=30)
# plt.title('Dispersion Curve', fontsize=40)

