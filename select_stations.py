import obspy
from pyproj import Geod
import numpy as np
geodist             = Geod(ellps='WGS84')

inv         = obspy.read_inventory('ALASKA_BH.xml')

new_inv     = obspy.core.inventory.Inventory(
    # We'll add networks later.
    networks=[],
    # The source should be the id whoever create the file.
    source="GLIMS")
nsta = 0

glims_inarr = np.loadtxt('/home/leon/glims_db/glims_download_06652/glims_points.gmt')
lons_glims  = glims_inarr[:, 0]
lats_glims  = glims_inarr[:, 1]

for network in inv:
    net     = obspy.core.inventory.Network(
                code=network.code,
                # A list of stations. We'll add one later.
                stations=[],
                description="GLIMS")

    for station in network:
        # if stacode != None:
        #     if station.code != stacode:
        #         continue
        # if station.code == 'DHY':
        # time            = obspy.UTCDateTime('20140101')
        # if station.end_date < time:
        #     continue
        # time            = obspy.UTCDateTime('20190229')
        # if station.start_date > time:
        #     continue
        az, baz, dist   = geodist.inv(np.ones(lons_glims.size)*station.longitude, np.ones(lons_glims.size)*station.latitude,\
                                              lons_glims, lats_glims)
        if dist.min() > 2000.:
            continue
        nsta    += 1
        net.stations.append(station)
    if len(net)>0:
        new_inv += net