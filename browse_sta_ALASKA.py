import seismicbrowser
import obspy

# dset    = seismicbrowser.browseASDF('ALASKA_LHZ_TA_AK.h5')
# dset.get_stations(minlatitude=52., maxlatitude=72.5, minlongitude=-172., maxlongitude=-122., channel='LHZ', startafter='20140101', network='TA,AK')
# dset.write_inv('ALASKA_TA_AK.xml')
# dset.read_inv('ALASKA_TA_AK.xml')


dset    = seismicbrowser.browseASDF('ALASKA_BH.h5')
# dset.get_stations(minlatitude=52., maxlatitude=72.5, minlongitude=-172., maxlongitude=-122., channel='BH*', startafter='19910101')
# dset.write_inv('ALASKA_BH.xml')
dset.read_inv('ALASKA_BH.xml')


dset.plot_inv()