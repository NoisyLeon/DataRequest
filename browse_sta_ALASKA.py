import seismicbrowser
import obspy

dset    = seismicbrowser.browseASDF('ALASKA.asdf')
# dset.get_stations(minlatitude=52., maxlatitude=72.5, minlongitude=-172., maxlongitude=-122., channel='LHZ')
# dset.write_inv('ALASKA.xml')
dset.read_inv('ALASKA.xml')