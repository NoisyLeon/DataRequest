import matplotlib.pyplot as plt
import obspy
import numpy as np
st = obspy.Stream()
st += obspy.read('/work3/leon/breq_fast/freq_no_time_no/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_no_time_one/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_no_time_run/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_yes_time_no/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_yes_time_one/COR_ANMO_HRV.SAC')
st += obspy.read('/work3/leon/breq_fast/freq_yes_time_run/COR_ANMO_HRV.SAC')

st.filter(type='bandpass', freqmin=0.01, freqmax=0.05, corners=4)
time = -3000.+np.arange(6001.)
# 
fig = plt.figure()
#
for i in xrange(len(st)):
    numb = 610+(i+1)
    ax = fig.add_subplot(numb)
    plt.plot(time, st[i], 'k', lw=1)
    ax.tick_params(axis='x', labelsize=20)
    plt.xlabel( 'Time (sec)', fontsize=30)
    # ax.tick_params(axis='y', labelsize=20)
# 
# 
# # plt.xlabel( 'Time (sec)', fontsize=30)
# plt.xlim([1000, 7200])
# ax.tick_params(axis='x', labelsize=20)
# ax.tick_params(axis='y', labelsize=20)
# ax = fig.add_subplot(312)
# # fig, ax = plt.subplots(312)
# plt.plot(time, data1, 'k', lw=2)
# # plt.xlabel( 'Time (sec)', fontsize=30)
# ax.tick_params(axis='x', labelsize=20)
# ax.tick_params(axis='y', labelsize=20)
# plt.xlim([1000, 7200])
# plt.ylim([-1.2, 1.2])
# ax = fig.add_subplot(313)
# # fig, ax = plt.subplots(313)
# plt.plot(time, data3, 'k', lw=2)
# plt.xlabel( 'Time (sec)', fontsize=30)
# ax.tick_params(axis='x', labelsize=20)
# ax.tick_params(axis='y', labelsize=20)
# plt.xlim([1000, 7200])
plt.show()


