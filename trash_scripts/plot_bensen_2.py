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

st.filter(type='bandpass', freqmin=0.01, freqmax=0.1, corners=4)
time = -3000.+np.arange(6001.)
# 
fig = plt.figure()
#
for i in xrange(len(st)):
    numb = 610+(i+1)
    st[i].data = st[i].data/max(st[i].data.max(), np.abs(st[i].data.min()))
    ax = fig.add_subplot(numb)
    plt.plot(time, st[i].data, 'k', lw=1)
    ax.tick_params(axis='x', labelsize=20)
    plt.xlabel( 'Time (sec)', fontsize=30)
    x=time; y=st[i].data
    ax.fill_between(x, -1.5, 1.5, where=(x > -500)*(x<500), facecolor='grey', alpha=0.3, linestyle='-')
    ax.fill_between(x, -1.5, 1.5, where=(x > 1500)*(x<2500), facecolor='grey', alpha=0.6, linestyle='--')
    # ax.fill_between(x, y.min()-0.3, y.max()+0.3, where=(x > 500)*(x<1500), facecolor='red', alpha=0.5)
    plt.ylim([-1., 1.])
    ax.yaxis.set_major_formatter(plt.NullFormatter())
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


