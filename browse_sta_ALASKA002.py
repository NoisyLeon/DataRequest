import seismicbrowser
import obspy
import GeoPolygon



# dset    = seismicbrowser.browseASDF('ALASKA_20181130_BHZ.h5')
dset    = seismicbrowser.browseASDF('ALASKA_BH.h5')
# dset.get_stations(latitude=61.3, longitude=-150., maxradius = 1., channel='BHZ', startbefore='20180601')
# dset.write_inv('ALASKA_20181130_BHZ.xml')
dset.read_inv('glims_5000.xml')
# 
# geopoly = GeoPolygon.GeoPolygonLst()
# geopoly.ReadGeoPolygonLst('/home/leon/glims_db/glims_download_06652/glims_lines.gmt')
# dset.plot_inv()





