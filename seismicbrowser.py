
import pyasdf
from obspy.clients.fdsn.client import Client
import obspy.clients.iris
import os
os.environ['PROJ_LIB'] = '/home/lili/anaconda3/share/proj'
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import matplotlib.pyplot as plt
import obspy
import numpy as np
from pyproj import Geod
geodist             = Geod(ellps='WGS84')
mondict = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}

def plot_fault_lines(mapobj, infname, lw=2, color='red'):
    with open(infname, 'rb') as fio:
        is_new  = False
        lonlst  = []
        latlst  = []
        for line in fio.readlines():
            if line.split()[0] == '>':
                x, y  = mapobj(lonlst, latlst)
                mapobj.plot(x, y,  lw = lw, color=color)
                # # # m.plot(xslb, yslb,  lw = 3, color='white')
                lonlst  = []
                latlst  = []
                continue
            lonlst.append(float(line.split()[0]))
            latlst.append(float(line.split()[1]))
        x, y  = mapobj(lonlst, latlst)
        mapobj.plot(x, y,  lw = lw, color=color)
            
    

class browseASDF(pyasdf.ASDFDataSet):
    
    def get_limits_lonlat(self):
        """Get the geographical limits of the stations
        """
        staLst  = self.waveforms.list()
        minlat  = 90.
        maxlat  = -90.
        minlon  = 360.
        maxlon  = 0.
        for staid in staLst:
            tmppos  = self.waveforms[staid].coordinates
            lat     = tmppos['latitude']
            lon     = tmppos['longitude']
            elv     = tmppos['elevation_in_m']
            if lon<0:
                lon += 360.
            minlat  = min(lat, minlat)
            maxlat  = max(lat, maxlat)
            minlon  = min(lon, minlon)
            maxlon  = max(lon, maxlon)
        print ('latitude range: ', minlat, '-', maxlat, 'longitude range:', minlon, '-', maxlon)
        self.minlat=minlat; self.maxlat=maxlat; self.minlon=minlon; self.maxlon=maxlon
        return
    
    def get_stations(self, startdate=None, enddate=None,  startbefore=None, startafter=None, endbefore=None, endafter=None,\
            network=None, station=None, location=None, channel=None, includerestricted=False,\
            minlatitude=None, maxlatitude=None, minlongitude=None, maxlongitude=None, latitude=None, longitude=None, minradius=None, maxradius=None):
        """Get station inventory from IRIS server
        =======================================================================================================
        Input Parameters:
        startdate, enddata  - start/end date for searching
        network             - Select one or more network codes.
                                Can be SEED network codes or data center defined codes.
                                    Multiple codes are comma-separated (e.g. "IU,TA").
        station             - Select one or more SEED station codes.
                                Multiple codes are comma-separated (e.g. "ANMO,PFO").
        location            - Select one or more SEED location identifiers.
                                Multiple identifiers are comma-separated (e.g. "00,01").
                                As a special case ?--? (two dashes) will be translated to a string of two space
                                characters to match blank location IDs.
        channel             - Select one or more SEED channel codes.
                                Multiple codes are comma-separated (e.g. "BHZ,HHZ").
        includerestricted   - default is False
        minlatitude         - Limit to events with a latitude larger than the specified minimum.
        maxlatitude         - Limit to events with a latitude smaller than the specified maximum.
        minlongitude        - Limit to events with a longitude larger than the specified minimum.
        maxlongitude        - Limit to events with a longitude smaller than the specified maximum.
        latitude            - Specify the latitude to be used for a radius search.
        longitude           - Specify the longitude to the used for a radius search.
        minradius           - Limit to events within the specified minimum number of degrees from the
                                geographic point defined by the latitude and longitude parameters.
        maxradius           - Limit to events within the specified maximum number of degrees from the
                                geographic point defined by the latitude and longitude parameters.
        =======================================================================================================
        """
        try:
            starttime   = obspy.core.utcdatetime.UTCDateTime(startdate)
        except:
            starttime   = None
        try:
            endtime     = obspy.core.utcdatetime.UTCDateTime(enddate)
        except:
            endtime     = None
        try:
            startbefore = obspy.core.utcdatetime.UTCDateTime(startbefore)
        except:
            startbefore = None
        try:
            startafter  = obspy.core.utcdatetime.UTCDateTime(startafter)
        except:
            startafter  = None
        try:
            endbefore   = obspy.core.utcdatetime.UTCDateTime(endbefore)
        except:
            endbefore   = None
        try:
            endafter    = obspy.core.utcdatetime.UTCDateTime(endafter)
        except:
            endafter    = None
        client          = Client('IRIS')
        inv             = client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, startbefore=startbefore, startafter=startafter,\
                                endbefore=endbefore, endafter=endafter, channel=channel, minlatitude=minlatitude, maxlatitude=maxlatitude, \
                                minlongitude=minlongitude, maxlongitude=maxlongitude, latitude=latitude, longitude=longitude, minradius=minradius, \
                                    maxradius=maxradius, level='channel', includerestricted=includerestricted)
        self.add_stationxml(inv)
        try:
            self.inv    += inv
        except:
            self.inv    = inv
        return
    
    def read_TA_lst(self, infname, startdate=None, enddate=None,  startbefore=None, startafter=None, endbefore=None, endafter=None, location=None, channel=None,\
            includerestricted=False, minlatitude=None, maxlatitude=None, minlongitude=None, maxlongitude=None, \
            latitude=None, longitude=None, minradius=None, maxradius=None):
        """Get station inventory from IRIS server
        =======================================================================================================
        Input Parameters:
        startdate, enddata  - start/end date for searching
        network             - Select one or more network codes.
                                Can be SEED network codes or data center defined codes.
                                    Multiple codes are comma-separated (e.g. "IU,TA").
        station             - Select one or more SEED station codes.
                                Multiple codes are comma-separated (e.g. "ANMO,PFO").
        location            - Select one or more SEED location identifiers.
                                Multiple identifiers are comma-separated (e.g. "00,01").
                                As a special case ?--? (two dashes) will be translated to a string of two space
                                characters to match blank location IDs.
        channel             - Select one or more SEED channel codes.
                                Multiple codes are comma-separated (e.g. "BHZ,HHZ").
        includerestricted   - default is False
        minlatitude         - Limit to events with a latitude larger than the specified minimum.
        maxlatitude         - Limit to events with a latitude smaller than the specified maximum.
        minlongitude        - Limit to events with a longitude larger than the specified minimum.
        maxlongitude        - Limit to events with a longitude smaller than the specified maximum.
        latitude            - Specify the latitude to be used for a radius search.
        longitude           - Specify the longitude to the used for a radius search.
        minradius           - Limit to events within the specified minimum number of degrees from the
                                geographic point defined by the latitude and longitude parameters.
        maxradius           - Limit to events within the specified maximum number of degrees from the
                                geographic point defined by the latitude and longitude parameters.
        =======================================================================================================
        """
        try:
            starttime   = obspy.core.utcdatetime.UTCDateTime(startdate)
        except:
            starttime   = None
        try:
            endtime     = obspy.core.utcdatetime.UTCDateTime(enddate)
        except:
            endtime     = None
        try:
            startbefore = obspy.core.utcdatetime.UTCDateTime(startbefore)
        except:
            startbefore = None
        try:
            startafter  = obspy.core.utcdatetime.UTCDateTime(startafter)
        except:
            startafter  = None
        try:
            endbefore   = obspy.core.utcdatetime.UTCDateTime(endbefore)
        except:
            endbefore   = None
        try:
            endafter    = obspy.core.utcdatetime.UTCDateTime(endafter)
        except:
            endafter    = None
        client          = Client('IRIS')
        init_flag       = True
        with open(infname, 'rb') as fio:
            for line in fio.readlines():
                network = line.split()[1]
                station = line.split()[2]
                if network == 'NET':
                    continue
                # print network, station
                if init_flag:
                    try:
                        inv     = client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, startbefore=startbefore, startafter=startafter,\
                                    endbefore=endbefore, endafter=endafter, channel=channel, minlatitude=minlatitude, maxlatitude=maxlatitude, \
                                        minlongitude=minlongitude, maxlongitude=maxlongitude, latitude=latitude, longitude=longitude, minradius=minradius, \
                                            maxradius=maxradius, level='channel', includerestricted=includerestricted)
                    except:
                        print ('No station inv: ', line)
                        continue
                    init_flag   = False
                    continue
                try:
                    inv     += client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, startbefore=startbefore, startafter=startafter,\
                                endbefore=endbefore, endafter=endafter, channel=channel, minlatitude=minlatitude, maxlatitude=maxlatitude, \
                                    minlongitude=minlongitude, maxlongitude=maxlongitude, latitude=latitude, longitude=longitude, minradius=minradius, \
                                        maxradius=maxradius, level='channel', includerestricted=includerestricted)
                except:
                    # for i in range(10):
                    #     try:
                    #         inv += client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, startbefore=startbefore, startafter=startafter,\
                    #             endbefore=endbefore, endafter=endafter, channel=channel, minlatitude=minlatitude, maxlatitude=maxlatitude, \
                    #                 minlongitude=minlongitude, maxlongitude=maxlongitude, latitude=latitude, longitude=longitude, minradius=minradius, \
                    #                     maxradius=maxradius, level='channel', includerestricted=includerestricted)
                    #     except:
                    print ('No station inv: ', line)
                    continue
                    # if i >= 9:
                        # print 'No station inv: ', line
        self.add_stationxml(inv)
        try:
            self.inv    += inv
        except:
            self.inv    = inv
        return
    
    def avg_dist(self, projection='lambert', geopolygons=None, showfig=True, blon=1, blat=1, \
                 netcodelist=[], plotetopo=True, stacode=None):
        """Plot station map
        ==============================================================================
        Input Parameters:
        projection      - type of geographical projection
        geopolygons     - geological polygons for plotting
        blon, blat      - extending boundaries in longitude/latitude
        showfig         - show figure or not
        ==============================================================================
        """
        inv         = self.inv
        inet        = 0
        stalons     = np.array([])
        stalats     = np.array([])
        for network in inv:
            # stalons     = np.array([])
            # stalats     = np.array([])
            if len(netcodelist) != 0:
                if network.code not in netcodelist:
                    continue
            inet        += 1
            for station in network:
                stalons         = np.append(stalons, station.longitude)
                stalats         = np.append(stalats, station.latitude)
        Nsta        = stalons.size
        g           = Geod(ellps='WGS84')
        distArr     = np.zeros(Nsta)
        # return abs(stalats - stalats[0])>0.1, stalons
        for ista in range(Nsta):
            lon     = stalons[ista]
            lat     = stalats[ista]
            ind     = (abs(stalons - lon)>0.1) + (abs(stalats - lat)>0.1)
            tlons   = stalons[ind]
            tlats   = stalats[ind]
            L       = tlons.size
            clonArr         = np.ones(L, dtype=float)*lon
            clatArr         = np.ones(L, dtype=float)*lat
            az, baz, dist   = g.inv(clonArr, clatArr, tlons, tlats)
            distArr[ista]   = dist.min()/1000.
            
        return distArr
    
    def avg_dist2(self, projection='lambert', geopolygons=None, showfig=True, blon=1, blat=1, \
                 netcodelist=[], plotetopo=True, stacode=None):
        """Plot station map
        ==============================================================================
        Input Parameters:
        projection      - type of geographical projection
        geopolygons     - geological polygons for plotting
        blon, blat      - extending boundaries in longitude/latitude
        showfig         - show figure or not
        ==============================================================================
        """
        staLst         = self.waveforms.list()
        inet        = 0
        stalons     = np.array([])
        stalats     = np.array([])
        for staid in staLst:
            lon     = self.waveforms[staid].StationXML.networks[0].stations[0].longitude
            lat     = self.waveforms[staid].StationXML.networks[0].stations[0].latitude
            stalons         = np.append(stalons, lon)
            stalats         = np.append(stalats, lat)

        Nsta        = stalons.size
        g           = Geod(ellps='WGS84')
        distArr     = np.zeros(Nsta)
        # return abs(stalats - stalats[0])>0.1, stalons
        for ista in range(Nsta):
            lon     = stalons[ista]
            lat     = stalats[ista]
            ind     = (abs(stalons - lon)>0.1) + (abs(stalats - lat)>0.1)
            tlons   = stalons[ind]
            tlats   = stalats[ind]
            L       = tlons.size
            clonArr         = np.ones(L, dtype=float)*lon
            clatArr         = np.ones(L, dtype=float)*lat
            az, baz, dist   = g.inv(clonArr, clatArr, tlons, tlats)
            distArr[ista]   = dist.min()/1000.
            
        return distArr
    
    def deploytime(self, projection='lambert', geopolygons=None, showfig=True, blon=1, blat=1, \
                 netcodelist=[], plotetopo=True, stacode=None):
        """Plot station map
        ==============================================================================
        Input Parameters:
        projection      - type of geographical projection
        geopolygons     - geological polygons for plotting
        blon, blat      - extending boundaries in longitude/latitude
        showfig         - show figure or not
        ==============================================================================
        """
        days        = np.array([])
        inv         = self.inv
        inet        = 0
        # lfdate1     = obspy.UTCDateTime('2019-02-28')
        lfdate      = obspy.UTCDateTime('2019-02-28')
        for network in inv:
            if len(netcodelist) != 0:
                if network.code not in netcodelist:
                    continue
            inet        += 1
            for station in network:
                sdate       = station.start_date
                edate       = station.end_date
                if edate > lfdate:
                    edate   = lfdate
                d           = (edate-sdate)/24./3600.
                if d < 0:
                    continue
                days        = np.append(days, d)
        return days
    
    def deploytime2(self, projection='lambert', geopolygons=None, showfig=True, blon=1, blat=1, \
                 netcodelist=[], plotetopo=True, stacode=None):
        """Plot station map
        ==============================================================================
        Input Parameters:
        projection      - type of geographical projection
        geopolygons     - geological polygons for plotting
        blon, blat      - extending boundaries in longitude/latitude
        showfig         - show figure or not
        ==============================================================================
        """
        staLst      = self.waveforms.list()
        inet        = 0
        days        = np.array([])
        cvdate1     = obspy.UTCDateTime('2005-01-01')
        cvdate      = obspy.UTCDateTime('2015-06-30')
        for staid in staLst:
            station     = self.waveforms[staid].StationXML[0][0]
            sdate       = station.start_date
            edate       = station.end_date
            if sdate < cvdate1:
                sdate   = cvdate1
            if edate > cvdate:
                edate   = cvdate
            d           = (edate-sdate)/24./3600.
            if d < 0:
                continue
            # if d >= 10000.:
            #     return sdate, edate
            days        = np.append(days, d)
        return days
    
    
    
    def write_inv(self, outfname, format='stationxml'):
        self.inv.write(outfname, format=format)
        return
    
    def read_inv(self, infname):
        self.inv    = obspy.core.inventory.inventory.read_inventory(infname)
        return
    
    def check_access(self):
        for net in self.inv:
            for sta in net:
                if sta.restricted_status != 'open':
                    print (sta)
        return
    
    def get_date(self):
        start_date  =  obspy.UTCDateTime('2599-12-31T23:59:59.000000Z')
        end_date    =  obspy.UTCDateTime(0)
        for net in self.inv:
            for sta in net:
                if sta.start_date < start_date:
                    start_date      = sta.start_date
                    self.sta_start  = sta
                    
                if sta.end_date > end_date:
                    end_date    = sta.end_date
                    self.sta_end= sta
        self.start_date = start_date
        self.end_date   = end_date
        
    def write_txt(self, outfname):
        with open(outfname, 'w') as fid:
            for staid in self.waveforms.list():
                temp    = staid.split('.')
                network = temp[0]
                stacode = temp[1]
                fid.writelines(stacode+' '+network+'\n')
        return
    
    def write_anxcorr_txt(self, outfname, start_date=obspy.UTCDateTime('2018-01-01'),\
                        end_date=obspy.UTCDateTime('2018-12-31')):
        temp_inv    = None
        with open(outfname, 'w') as fid:
            for staid in self.waveforms.list():
                st_date = self.waveforms[staid].StationXML.networks[0].stations[0].start_date
                ed_date = self.waveforms[staid].StationXML.networks[0].stations[0].end_date
                if st_date > end_date or ed_date < start_date:
                    continue
                temp    = staid.split('.')
                network = temp[0]
                stacode = temp[1]
                stlo    = self.waveforms[staid].StationXML.networks[0].stations[0].longitude
                stla    = self.waveforms[staid].StationXML.networks[0].stations[0].latitude
                fid.writelines(stacode+' '+str(stlo)+' '+str(stla)+' '+network+'\n')
                if temp_inv is None:
                    temp_inv    = self.waveforms[staid].StationXML
                else:
                    temp_inv    += self.waveforms[staid].StationXML
                    
        self.inv    = temp_inv
        return
    
    def write_pairs(self, outfname):
        distlst     = []
        stalst1     = []
        stalst2     = []
        networks    = ['TA', 'AK', 'AV', 'AT']
        for staid1 in self.waveforms.list():
            for staid2 in self.waveforms.list():
                if staid1 >= staid2:
                    continue
                temp        = staid1.split('.')
                network1    = temp[0]
                stacode1    = temp[1]
                temp        = staid2.split('.')
                network2    = temp[0]
                stacode2    = temp[1]
                if not network1 in networks:
                    continue
                if not network2 in networks:
                    continue
                stla1           = self.waveforms[staid1].coordinates['latitude']
                stlo1           = self.waveforms[staid1].coordinates['longitude']
                stla2           = self.waveforms[staid2].coordinates['latitude']
                stlo2           = self.waveforms[staid2].coordinates['longitude']
                dist, az, baz   = obspy.geodetics.gps2dist_azimuth(stla1, stlo1, stla2, stlo2) # distance is in m
                dist            /= 1000.
                distlst.append(dist)
                stalst1.append(staid1)
                stalst2.append(staid2)
        distlst = np.asarray([distlst])
        # distlst = distlst.reshape(distlst.size)
        indlst  = np.argsort(distlst)[0]
        # return distlst
        # print indlst, distlst
        # print len(indlst), distlst.size, len(stalst2)
        with open(outfname, 'w') as fid:
            for ind in indlst:
                fid.writelines(stalst1[ind]+' '+stalst2[ind]+' '+str(distlst[0, ind])+'\n')
        return
    
    def _get_basemap(self, projection='lambert', geopolygons=None, resolution='i', blon=0., blat=0.):
        """Get basemap for plotting results
        """
        fig=plt.figure(num=None, figsize=(12, 12), dpi=100, facecolor='w', edgecolor='k')
        try:
            minlon  = self.minlon-blon
            maxlon  = self.maxlon+blon
            minlat  = self.minlat-blat
            maxlat  = self.maxlat+blat
        except AttributeError:
            self.get_limits_lonlat()
            minlon  = self.minlon-blon; maxlon=self.maxlon+blon; minlat=self.minlat-blat; maxlat=self.maxlat+blat
        # minlon      = 188 - 360.
        # maxlon      = 238. - 360.
        # minlat      = 52.
        # maxlat      = 72.
        lat_centre  = (maxlat+minlat)/2.0
        lon_centre  = (maxlon+minlon)/2.0
        if projection == 'merc':
            m       = Basemap(projection='merc', llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon,
                      urcrnrlon=maxlon, lat_ts=0, resolution=resolution)
            m.drawparallels(np.arange(-80.0,80.0,5.0), labels=[1,1,1,1], fontsize=15)
            m.drawmeridians(np.arange(-170.0,170.0,10.0), labels=[1,1,1,1], fontsize=15)
        elif projection == 'global':
            m       = Basemap(projection='ortho',lon_0=lon_centre, lat_0=lat_centre, resolution=resolution)
        elif projection == 'regional_ortho':
            m1      = Basemap(projection='ortho', lon_0=minlon, lat_0=minlat, resolution='l')
            m       = Basemap(projection='ortho', lon_0=minlon, lat_0=minlat, resolution=resolution,\
                        llcrnrx=0., llcrnry=0., urcrnrx=m1.urcrnrx/mapfactor, urcrnry=m1.urcrnry/3.5)
            m.drawparallels(np.arange(-80.0,80.0,10.0), labels=[1,0,0,0],  linewidth=2,  fontsize=20)
            m.drawmeridians(np.arange(-170.0,170.0,10.0),  linewidth=2)
        elif projection=='lambert':
            distEW, az, baz = obspy.geodetics.gps2dist_azimuth((lat_centre+minlat)/2., minlon, (lat_centre+minlat)/2., maxlon-15) # distance is in m
            distNS, az, baz = obspy.geodetics.gps2dist_azimuth(minlat, minlon, maxlat-6, minlon) # distance is in m
            m       = Basemap(width=distEW, height=distNS, rsphere=(6378137.00,6356752.3142), resolution='l', projection='lcc',\
                        lat_1=minlat, lat_2=maxlat, lon_0=lon_centre-2., lat_0=lat_centre+2.4)
            m.drawparallels(np.arange(-80.0,80.0,5.0), linewidth=1., dashes=[2,2], labels=[1,1,0,1], fontsize=15)
            m.drawmeridians(np.arange(-170.0,170.0,10.0), linewidth=1., dashes=[2,2], labels=[0,0,1,1], fontsize=15)
        elif projection == 'ortho':
            m       = Basemap(projection='ortho', lon_0=(minlon+maxlon)/2., lat_0=(minlat+maxlat)/2., resolution='l')
            m.drawparallels(np.arange(-80.0,80.0,10.0), labels=[1,0,0,0],  linewidth=1,  fontsize=20)
            m.drawmeridians(np.arange(-180.0,180.0,10.0),  linewidth=1)
        # m.drawcoastlines(linewidth=0.2)
        
        coasts = m.drawcoastlines(zorder=100,color= '0.9',linewidth=0.001)
        
        # Exact the paths from coasts
        coasts_paths = coasts.get_paths()
        poly_stop = 23
        for ipoly in range(len(coasts_paths)):
            print (ipoly)
            if ipoly > poly_stop:
                break
            r = coasts_paths[ipoly]
            # Convert into lon/lat vertices
            polygon_vertices = [(vertex[0],vertex[1]) for (vertex,code) in
                                r.iter_segments(simplify=False)]
            px = [polygon_vertices[i][0] for i in range(len(polygon_vertices))]
            py = [polygon_vertices[i][1] for i in range(len(polygon_vertices))]
            
            m.plot(px,py,'k-',linewidth=.5)
        m.drawcountries(linewidth=1.)
        try:
            geopolygons.PlotPolygon(inbasemap=m)
        except:
            pass
        return m
    
    def plot_stations(self, projection='lambert', geopolygons=None, showfig=True, blon=.5, blat=0.5):
        """Plot station map
        ==============================================================================
        Input Parameters:
        projection      - type of geographical projection
        geopolygons     - geological polygons for plotting
        blon, blat      - extending boundaries in longitude/latitude
        showfig         - show figure or not
        ==============================================================================
        """
        staLst  = self.waveforms.list()
        stalons = np.array([])
        stalats = np.array([])
        for staid in staLst:
            tmppos          = self.waveforms[staid].coordinates
            tmppos  = self.waveforms[staid].coordinates
            lat     = tmppos['latitude']
            lon     = tmppos['longitude']
            evz     = tmppos['elevation_in_m']
            stalons         = np.append(stalons, lon)
            stalats         = np.append(stalats, lat)
        m                   = self._get_basemap(projection=projection, geopolygons=geopolygons, blon=blon, blat=blat)
        # m.warpimage(image='etopo1')
        # m.warpimage(image='https://www.ngdc.noaa.gov/mgg/image/color_etopo1_ice_low.jpg')
        # m.shadedrelief()
        # m.etopo()
        stax, stay          = m(stalons, stalats)
        m.plot(stax, stay, 'r^', markersize=10)
        # plt.title(str(self.period)+' sec', fontsize=20)
        if showfig:
            plt.show()
        return
    
           
        
        
        
    
    