import seismicbrowser
import obspy

dset    = seismicbrowser.browseASDF('TEST_LH.h5')
dset.get_stations(channel='LH?', network='IU', station='HRV,ANMO')
# dset.get_stations(minlatitude=-17.78, maxlatitude=4.15, minlongitude=23.00, maxlongitude=40.2, channel='LH?', startafter='19940101')
# dset.write_inv('EARS_LH.xml')
#dset.read_inv('EARS_LH.xml')
#dset.write_txt(outfname='ASN/EARS_LH_breqfast.txt')
# 


# dset    = seismicbrowser.browseASDF('ALASKA_LH.h5')
# # dset.get_stations(minlatitude=52., maxlatitude=72.5, minlongitude=-172., maxlongitude=-122., channel='BH*', startafter='19910101')
# # dset.write_inv('ALASKA_BH.xml')
# dset.read_inv('ALASKA.xml')
# # # # 
# # # # 
# # # # dset.plot_inv(netcodelist=['AK', 'TA', 'XN', 'XY', 'AV', 'PO', 'US', 'CN'])
# # dset.plot_topo()
# # dset.plot_inv(projection='merc')
# dset.plot_inv2(plotetopo=True)





