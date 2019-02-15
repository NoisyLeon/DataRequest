import seismicbrowser
import obspy

dset    = seismicbrowser.browseASDF('USCON_TA.h5')
dset.read_TA_lst(infname='_US-TA-StationList.txt', channel='LHE,LHN,LHZ', maxlatitude=50.)

# dset.write_inv('ALASKA_TA_AK.xml')
# dset.read_inv('ALASKA_TA_AK.xml')
# 
# 
# dset    = seismicbrowser.browseASDF('ALASKA_BH.h5')
# # dset.get_stations(minlatitude=52., maxlatitude=72.5, minlongitude=-172., maxlongitude=-122., channel='BH*', startafter='19910101')
# # dset.write_inv('ALASKA_BH.xml')
# dset.read_inv('ALASKA_BH.xml')
# 
# 
# dset.plot_inv()