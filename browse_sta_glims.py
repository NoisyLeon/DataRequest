import seismicbrowser
import obspy
import GeoPolygon




# dset    = seismicbrowser.browseASDF('glims_BH.h5')
dset    = seismicbrowser.browseASDF('ALASKA_BH.h5')
# dset.read_inv('glims_5000.xml')
# dset.read_inv('ALASKA_BH.xml')
dset.write_anxcorr_txt('sta_glims.lst')





