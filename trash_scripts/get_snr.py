import matplotlib.pyplot as plt
import obspy
import numpy as np
import obspy.signal

st = obspy.Stream()
st += obspy.read('/work3/leon/breq_fast/freq_no_time_no/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_no_time_one/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_no_time_run/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_yes_time_no/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_yes_time_one/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_yes_time_run/COR_ANMO_HRV.SAC')

st.filter(type='bandpass', freqmin=0.05, freqmax=0.1, corners=4)

for i in xrange(len(st)):
    pre_tr  = st[i].copy()
    coda_tr = st[i].copy()
    pos_tr  = st[i].copy()
    stime   = st[i].stats.starttime
    pre_tr.trim(starttime=stime+2500, endtime=stime+3500)
    coda_tr.trim(starttime=stime+4500, endtime=stime+5000)
    pos_tr.trim(starttime=stime+3500)
    pre_rms = np.sqrt(np.mean(pre_tr.data**2))
    coda_rms= np.sqrt(np.mean(coda_tr.data**2))
    pos_env = obspy.signal.filter.envelope(pos_tr.data)
    Amax    = pos_env.max()
    # print pre_rms, coda_rms, Amax, Amax/pre_rms, Amax/coda_rms
    print Amax/pre_rms, Amax/coda_rms
    