import seismicbrowser
import obspy

dset    = seismicbrowser.browseASDF('USCON_TA.h5')
# dset.read_TA_lst(infname='_US-TA-StationList.txt', channel='LHE,LHN,LHZ', maxlatitude=50.)

# dset.write_inv('ALASKA_TA_AK.xml')
dset.read_inv('ALASKA_TA_AK.xml')
# 
# 
# dset    = seismicbrowser.browseASDF('ALASKA_BH.h5')
# # dset.get_stations(minlatitude=52., maxlatitude=72.5, minlongitude=-172., maxlongitude=-122., channel='BH*', startafter='19910101')
# # dset.write_inv('ALASKA_BH.xml')
# dset.read_inv('ALASKA_BH.xml')
# 
# 
# dset.plot_inv()
def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = '%.0f' %(100. * y)
    # s = str(y)
    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
ax = plt.subplot()
data = d1
weights = np.ones_like(data)/float(data.size)
desired_bin_size    = 20.
min_val = np.min(data)
max_val = np.max(data)
min_boundary = -1.0 * (min_val % desired_bin_size - min_val)
max_boundary = max_val - max_val % desired_bin_size + desired_bin_size

n_bins = int((max_boundary - min_boundary) / desired_bin_size) + 1
plt.hist(data, bins=n_bins, weights=weights, label='Lower 48', alpha=0.5)
# plt.hist(data, bins=n_bins, weights=weights, label='Love wave, %g sec'%( pers2[i] ))
outstd  = data.std()
outmean = data.mean()

data = d2
weights = np.ones_like(data)/float(data.size)
desired_bin_size    = 20.
min_val = np.min(data)
max_val = np.max(data)
min_boundary = -1.0 * (min_val % desired_bin_size - min_val)
max_boundary = max_val - max_val % desired_bin_size + desired_bin_size

n_bins = int((max_boundary - min_boundary) / desired_bin_size) + 1
plt.hist(data, bins=n_bins, weights=weights, label='Alaska', alpha=0.5)
# plt.hist(data, bins=n_bins, weights=weights, label='Love wave, %g sec'%( pers2[i] ))
outstd  = data.std()
outmean = data.mean()


from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter
formatter = FuncFormatter(to_percent)
# Set the formatter
plt.gca().yaxis.set_major_formatter(formatter)

plt.ylabel('Percentage (%)', fontsize=80)
# plt.xlabel('interstation distance (km)', fontsize=80)
plt.xlabel('days', fontsize=80)
plt.legend(fontsize=30)
# plt.xlim([0., 200.])
# plt.xlim([0., 200.])
ax.tick_params(axis='x', labelsize=50)
ax.tick_params(axis='y', labelsize=50)