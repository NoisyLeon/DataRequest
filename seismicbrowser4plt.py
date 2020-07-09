
import seismicbrowser
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
            
    

class browseASDF(seismicbrowser.browseASDF):
    
    def _get_basemap_plt(self, projection='lambert', geopolygons=None, resolution='i', blon=0., blat=0.):
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
    
    
    
    
    def plot_inv(self, projection='merc', geopolygons=None, showfig=True, blon=1, blat=1, \
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
        inv     = self.inv
        m       = self._get_basemap_plt(projection=projection, geopolygons=geopolygons, blon=blon, blat=blat)
        # m.etopo()
        if plotetopo:
            from netCDF4 import Dataset
            from matplotlib.colors import LightSource
            import pycpt
            etopodata   = Dataset('/home/leon/station_map/grd_dir/ETOPO1_Ice_g_gmt4.grd')
            etopo       = etopodata.variables['z'][:]
            lons        = etopodata.variables['x'][:]
            lats        = etopodata.variables['y'][:]
            
            # # # etopodata   = Dataset('/home/leon/GEBCO_2019.nc')
            # # # etopo       = etopodata.variables['elevation'][:]
            # # # lons        = etopodata.variables['lon'][:]
            # # # lats        = etopodata.variables['lat'][:]

            ind_lon     = (lons <= -122.)*(lons>=-180.)
            ind_lat     = (lats <= 75.)*(lats>=50.)
            # etopo       = etopo[ind_lat, ind_lon]
            tetopo      = etopo[ind_lat, :]
            etopo       = tetopo[:, ind_lon]
            lons        = lons[ind_lon]
            lats        = lats[ind_lat]
            ls          = LightSource(azdeg=315, altdeg=45)
            # nx          = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
            # etopo,lons  = shiftgrid(180.,etopo,lons,start=False)
            # topodat,x,y = m.transform_scalar(etopo,lons,lats,nx,ny,returnxy=True)
            ny, nx      = etopo.shape
            topodat,xtopo,ytopo = m.transform_scalar(etopo,lons,lats,nx, ny, returnxy=True)
            m.imshow(ls.hillshade(topodat, vert_exag=1., dx=1., dy=1.), cmap='gray')
            mycm1       = pycpt.load.gmtColormap('/home/leon/station_map/etopo1.cpt')
            mycm2       = pycpt.load.gmtColormap('/home/leon/station_map/bathy1.cpt')
            mycm2.set_over('w',0)
            m.imshow(ls.shade(topodat, cmap=mycm1, vert_exag=1., dx=1., dy=1., vmin=0, vmax=8000))
            m.imshow(ls.shade(topodat, cmap=mycm2, vert_exag=1., dx=1., dy=1., vmin=-11000, vmax=-0.5))
        
        # shapefname  = '/home/leon/geological_maps/qfaults'
        # m.readshapefile(shapefname, 'faultline', linewidth=2, color='red')
        # shapefname  = '/home/leon/AKgeol_web_shp/AKStategeolarc_generalized_WGS84'
        # m.readshapefile(shapefname, 'geolarc', linewidth=1, color='red')
        # shapefname  = '/home/leon/glims_db/glims_download_07183/glims_images'
        # m.readshapefile(shapefname, 'glims', linewidth=1, color='red')
        
        # import shapefile
        # shplst = shapefile.Reader("/home/leon/glims_db/glims_download_07183/glims_points.shp")
        # ishp    = 0
        # records = shplst.shapeRecords()
        # L       = len(records)
        # for shp in records:
        #     points      = shp.shape.points
        #     lon_glims   = []
        #     lat_glims   = []
        #     ishp        += 1
        #     print ishp, L
        #     for point in points:
        #         lon_glims.append(point[0])
        #         lat_glims.append(point[1])
        #     xglims, yglims      = m(lon_glims, lat_glims)
        #     m.plot(xglims, yglims,'-', ms = 15, markeredgecolor='grey', markerfacecolor='yellow')
        #######################3
        # glims_inarr = np.loadtxt('/home/leon/glims_db/glims_download_06652/glims_points.gmt')
        # lons_glims  = glims_inarr[:, 0]
        # lats_glims  = glims_inarr[:, 1]
        # xglims, yglims      = m(lons_glims, lats_glims)
        # m.plot(xglims, yglims,'o', ms = 2, markeredgecolor='cyan', markerfacecolor='cyan')
        #########################
        inet        = 0
        for network in inv:
            stalons     = np.array([])
            stalats     = np.array([])
            if len(netcodelist) != 0:
                if network.code not in netcodelist:
                    continue
            inet        += 1
            for station in network:
                # if stacode != None:
                #     if station.code != stacode:
                #         continue
                # if station.code == 'DHY':
                # time            = obspy.UTCDateTime('20150101')
                # if station.end_date < time:
                #     continue
                # time            = obspy.UTCDateTime('20141231')
                # if station.start_date > time:
                #     continue
                # az, baz, dist   = geodist.inv(np.ones(lons_glims.size)*station.longitude, np.ones(lons_glims.size)*station.latitude,\
                #                                       lons_glims, lats_glims)
                # if dist.min() > 5000.:
                #     continue
                stalons         = np.append(stalons, station.longitude)
                stalats         = np.append(stalats, station.latitude)
            stax, stay      = m(stalons, stalats)
            # if inet==1:
            #     m.plot(stax, stay, 'r^', mec='k', markersize=8, label = network.code)
            # if inet == 2:
            #     m.plot(stax, stay, 'b^', mec='k', markersize=8, label = network.code)
            # m.plot(stax, stay, 'r^', mec='k', markersize=20, label = network.code+'.'+stacode)
            # 
            # m.plot(stax, stay, 'r^', markersize=15)
            labellst    = ['r^', 'b^', 'm^', 'c^', 'w^', \
                           'ro', 'bo', 'mo', 'co',  'wo', \
                              'rv', 'bv', 'mv', 'cv',  'wv', \
                              'rs', 'bs', 'ms', 'cs',  'ws', \
                              'rp', 'bp', 'mp', 'cp',  'wp']
            # if network.code == 'TA':
            #     continue
            m.plot(stax, stay, labellst[inet-1], mec='k', markersize=8, label = network.code)
            # if inet<=10:
            #     m.plot(stax, stay, '^', mec='k', markersize=8, label = network.code)
            # elif inet > 10 and inet <=20:
            #     m.plot(stax, stay, 's', mec='k', markersize=8, label = network.code)
            # elif inet > 20:
            #     m.plot(stax, stay, 'v', mec='k', markersize=8, label = network.code)
        plt.legend(numpoints=1, loc=1, fontsize=10)
        #######################################
        # xc, yc      = m(np.array([-140]), np.array([63]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        # phi         = - 81.097
        # U       = np.sin(phi/180.*np.pi)
        # V       = np.cos(phi/180.*np.pi)
        # m.quiver(xc, yc, U, V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # m.quiver(xc, yc, -U, -V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # 
        # xc, yc      = m(np.array([-146]), np.array([65]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        # phi         = 75.8076
        # U       = np.sin(phi/180.*np.pi)
        # V       = np.cos(phi/180.*np.pi)
        # m.quiver(xc, yc, U, V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # m.quiver(xc, yc, -U, -V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # 
        # xc, yc      = m(np.array([-153]), np.array([64]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        # phi         = 53.1896
        # U       = np.sin(phi/180.*np.pi)
        # V       = np.cos(phi/180.*np.pi)
        # m.quiver(xc, yc, U, V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # m.quiver(xc, yc, -U, -V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # 
        # xc, yc      = m(np.array([-156]), np.array([62]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        # phi         = 32.1394
        # U       = np.sin(phi/180.*np.pi)
        # V       = np.cos(phi/180.*np.pi)
        # m.quiver(xc, yc, U, V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # m.quiver(xc, yc, -U, -V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        #######################################
        
        
        
        # xc, yc      = m(np.array([-140]), np.array([63]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        
        # xc, yc      = m(np.array([-146, -142]), np.array([58, 64]))
        # m.plot(xc, yc,'k', lw = 5, color='black')
        # m.plot(xc, yc,'k', lw = 3, color='white')
        # 
        # xc, yc      = m(np.array([-147, -159]), np.array([56, 62]))
        # m.plot(xc, yc,'k', lw = 5, color='black')
        # m.plot(xc, yc,'k', lw = 3, color='white')
        # plot_fault_lines(m, 'AK_Faults.txt')
        #
        # import shapefile
        # shapefname  = '/home/leon/volcano_locs/SDE_GLB_VOLC.shp'
        # shplst      = shapefile.Reader(shapefname)
        # for rec in shplst.records():
        #     lon_vol = rec[4]
        #     lat_vol = rec[3]
        #     xvol, yvol            = m(lon_vol, lat_vol)
        #     m.plot(xvol, yvol, '^', mfc='white', mec='k', ms=10)
        #
        #############################
        # yakutat_slb_dat     = np.loadtxt('YAK_extent.txt')
        # yatlons             = yakutat_slb_dat[:, 0]
        # yatlats             = yakutat_slb_dat[:, 1]
        # xyat, yyat          = m(yatlons, yatlats)
        # m.plot(xyat, yyat, '-', lw = 5, color='black')
        # m.plot(xyat, yyat, '-', lw = 3, color='white')
        #############################
        # plot_fault_lines(m, 'AK_Faults.txt', color='red')
        if showfig:
            plt.show()
        return
    
    def plot_topo(self, projection='lambert', geopolygons=None, showfig=True, blon=1, blat=1, \
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
        # inv     = self.inv
        m       = self._get_basemap_plt(projection=projection, geopolygons=geopolygons, blon=blon, blat=blat)
        # m.etopo()
        if plotetopo:
            from netCDF4 import Dataset
            from matplotlib.colors import LightSource
            import pycpt
            # # # etopodata   = Dataset('/home/leon/station_map/grd_dir/ETOPO2v2g_f4.nc')
            # # # etopo       = etopodata.variables['z'][:]
            # # # lons        = etopodata.variables['x'][:]
            # # # lats        = etopodata.variables['y'][:]
            etopodata   = Dataset('/home/leon/GEBCO_2019.nc')
            etopo       = etopodata.variables['elevation'][:]
            lons        = etopodata.variables['lon'][:]
            lats        = etopodata.variables['lat'][:]

            ind_lon     = (lons <= -123.)*(lons>=-180.)
            ind_lat     = (lats <= 75.)*(lats>=55.)
            # etopo       = etopo[ind_lat, ind_lon]
            tetopo      = etopo[ind_lat, :]
            etopo       = tetopo[:, ind_lon]
            lons        = lons[ind_lon]
            lats        = lats[ind_lat]
            
            
            ls          = LightSource(azdeg=315, altdeg=45)
            # nx          = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
            
            # etopo,lons  = shiftgrid(180., etopo, lons, start=False)
            
            # topodat,x,y = m.transform_scalar(etopo,lons,lats,nx,ny,returnxy=True)
            ny, nx      = etopo.shape
            topodat,xtopo,ytopo = m.transform_scalar(etopo,lons,lats,nx, ny, returnxy=True)
            m.imshow(ls.hillshade(topodat, vert_exag=1., dx=1., dy=1.), cmap='gray')
            mycm1       = pycpt.load.gmtColormap('/home/leon/station_map/etopo1.cpt')
            mycm2       = pycpt.load.gmtColormap('/home/leon/station_map/bathy1.cpt')
            mycm2.set_over('w',0)
            m.imshow(ls.shade(topodat, cmap=mycm1, vert_exag=1., dx=1., dy=1., vmin=0, vmax=8000))
            m.imshow(ls.shade(topodat, cmap=mycm2, vert_exag=1., dx=1., dy=1., vmin=-11000, vmax=-0.5))
        
        #############################
        yakutat_slb_dat     = np.loadtxt('YAK_extent.txt')
        yatlons             = yakutat_slb_dat[:, 0]
        yatlats             = yakutat_slb_dat[:, 1]
        xyat, yyat          = m(yatlons, yatlats)
        m.plot(xyat, yyat, '-', lw = 5, color='black')
        m.plot(xyat, yyat, '-', lw = 3, color='white')
        #############################

        plot_fault_lines(m, 'AK_Faults.txt', color='black')
        # #
        def read_slab_contour(infname, depth):
            ctrlst  = []
            lonlst  = []
            latlst  = []
            with open(infname, 'rb') as fio:
                newctr  = False
                for line in fio.readlines():
                    if line.split()[0] is '>':
                        newctr  = True
                        if len(lonlst) != 0:
                            ctrlst.append([lonlst, latlst])
                        lonlst  = []
                        latlst  = []
                        z       = -float(line.split()[1])
                        if z == depth:
                            skipflag    = False
                        else:
                            skipflag    = True
                        continue
                    if skipflag:
                        continue
                    lonlst.append(float(line.split()[0]))
                    latlst.append(float(line.split()[1]))
            return ctrlst
        dlst    = [40., 60., 80., 100.]
        # dlst    = [100.]
        
                # m.plot(xslb, yslb,  '--', lw = 3, color='white')
        #
        ####    
        arr             = np.loadtxt('SlabE325.dat')
        lonslb          = arr[:, 0]
        latslb          = arr[:, 1]
        depthslb        = -arr[:, 2]
        for depth in dlst:
                # index           = (depthslb > (depth - .05))*(depthslb < (depth + .05))
                index           = (depthslb == depth)
                lonslb2         = lonslb[index]
                latslb2         = latslb[index]
                indsort         = lonslb2.argsort()
                lonslb2         = lonslb2[indsort]
                latslb2         = latslb2[indsort]
                xslb, yslb      = m(lonslb2, latslb2)
                # m.plot(xslb, yslb,  '-', lw = 5, color='black')
                m.plot(xslb, yslb,  '-', lw = 3, color='red')
                                                     
        #############################
        # for depth in dlst:
        #     slb_ctrlst      = read_slab_contour('alu_contours.in', depth=depth)
        #     for slbctr in slb_ctrlst:
        #         xslb, yslb  = m(np.array(slbctr[0])-360., np.array(slbctr[1]))
        #         m.plot(xslb, yslb,  '--', lw = 3, color='red')
        ###
        
        import shapefile
        shapefname  = '/home/leon/volcano_locs/SDE_GLB_VOLC.shp'
        shplst      = shapefile.Reader(shapefname)
        for rec in shplst.records():
            lon_vol = rec[4]
            lat_vol = rec[3]
            xvol, yvol            = m(lon_vol, lat_vol)
            m.plot(xvol, yvol, '^', mfc='white', mec='k', ms=10)
        #
        #
        xc, yc      = m(np.array([-156]), np.array([67.5]))
        m.plot(xc, yc,'*', ms = 20, markeredgecolor='black', markerfacecolor='yellow')
        xc, yc      = m(np.array([-153]), np.array([61.]))
        m.plot(xc, yc,'*', ms = 20, markeredgecolor='black', markerfacecolor='yellow')
        xc, yc      = m(np.array([-149]), np.array([64.5]))
        m.plot(xc, yc,'*', ms = 20, markeredgecolor='black', markerfacecolor='yellow')        
        xc, yc      = m(np.array([-152]), np.array([60.]))
        m.plot(xc, yc,'*', ms = 20, markeredgecolor='black', markerfacecolor='yellow')
        if showfig:
            plt.show()
        return
    
    def plot_inv2(self, projection='lambert', geopolygons=None, showfig=True, blon=1, blat=1, \
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
        inv     = self.inv
        m       = self._get_basemap_plt(projection=projection, geopolygons=geopolygons, blon=blon, blat=blat)
        # m.etopo()
        if plotetopo:
            from netCDF4 import Dataset
            from matplotlib.colors import LightSource
            import pycpt
            # etopodata   = Dataset('/home/leon/station_map/grd_dir/ETOPO2v2g_f4.nc')
            # etopodata   = Dataset('/home/lili/data_marin/map_data/station_map/grd_dir/ETOPO1_Ice_g_gmt4.grd')
            # etopo       = etopodata.variables['z'][:]
            # lons        = etopodata.variables['x'][:]
            # lats        = etopodata.variables['y'][:]
            etopodata   = Dataset('/home/lili/gebco_alaska2.nc')
            etopo       = etopodata.variables['elevation'][:]
            lons        = etopodata.variables['lon'][:]
            lons[lons>180.] = lons[lons>180.] - 360.
            lats        = etopodata.variables['lat'][:]

            ind_lon     = (lons <= -120.)*(lons>=-180.)
            ind_lat     = (lats <= 75.)*(lats>=55.)
            # etopo       = etopo[ind_lat, ind_lon]
            tetopo      = etopo[ind_lat, :]
            etopo       = tetopo[:, ind_lon]
            lons        = lons[ind_lon]
            lats        = lats[ind_lat]
            
            ls          = LightSource(azdeg=315, altdeg=45)
            # nx          = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
            # etopo,lons  = shiftgrid(180.,etopo,lons,start=False)
            # topodat,x,y = m.transform_scalar(etopo,lons,lats,nx,ny,returnxy=True)
            ny, nx      = etopo.shape
            topodat,xtopo,ytopo = m.transform_scalar(etopo,lons,lats,nx, ny, returnxy=True)
            m.imshow(ls.hillshade(topodat, vert_exag=1., dx=1., dy=1.), cmap='gray')
            mycm1       = pycpt.load.gmtColormap('/home/lili/data_marin/map_data/station_map/etopo1.cpt_land')
            mycm2       = pycpt.load.gmtColormap('/home/lili/data_marin/map_data/station_map/bathy1.cpt')
            mycm2.set_over('w',0)
            m.imshow(ls.shade(topodat, cmap=mycm1, vert_exag=1., dx=1., dy=1., vmin=0., vmax=8000.))
            m.imshow(ls.shade(topodat, cmap=mycm2, vert_exag=1., dx=1., dy=1., vmin=-11000., vmax=-0.5))
        inet        = 0
        for network in inv:
            stalons     = np.array([])
            stalats     = np.array([])
            if len(netcodelist) != 0:
                if network.code not in netcodelist:
                    continue
            inet        += 1
            for station in network:
                # if stacode != None:
                #     if station.code != stacode:
                #         continue
                # if station.code == 'DHY':
                # time            = obspy.UTCDateTime('20150101')
                # if station.end_date < time:
                #     continue
                # time            = obspy.UTCDateTime('20141231')
                # if station.start_date > time:
                #     continue
                # az, baz, dist   = geodist.inv(np.ones(lons_glims.size)*station.longitude, np.ones(lons_glims.size)*station.latitude,\
                #                                       lons_glims, lats_glims)
                # if dist.min() > 5000.:
                #     continue
                stalons         = np.append(stalons, station.longitude)
                stalats         = np.append(stalats, station.latitude)
            stax, stay      = m(stalons, stalats)
            # if inet==1:
            #     m.plot(stax, stay, 'r^', mec='k', markersize=8, label = network.code)
            # if inet == 2:
            #     m.plot(stax, stay, 'b^', mec='k', markersize=8, label = network.code)
            # m.plot(stax, stay, 'r^', mec='k', markersize=20, label = network.code+'.'+stacode)
            # 
            # m.plot(stax, stay, 'r^', markersize=15)
            labellst    = ['r^', 'b^', 'm^', 'c^', 'w^', \
                           'ro', 'bo', 'mo', 'co',  'wo', \
                              'rv', 'bv', 'mv', 'cv',  'wv', \
                              'rs', 'bs', 'ms', 'cs',  'ws', \
                              'rp', 'bp', 'mp', 'cp',  'wp']

            # # # m.plot(stax, stay, labellst[inet-1], mec='k', markersize=8, label = network.code)
            m.plot(stax, stay, 'k^', mec='k', markersize=8, label = network.code)
            # if inet<=10:
            #     m.plot(stax, stay, '^', mec='k', markersize=8, label = network.code)
            # elif inet > 10 and inet <=20:
            #     m.plot(stax, stay, 's', mec='k', markersize=8, label = network.code)
            # elif inet > 20:
            #     m.plot(stax, stay, 'v', mec='k', markersize=8, label = network.code)
        # plt.legend(numpoints=1, loc=1, fontsize=10)
        #######################################
        # xc, yc      = m(np.array([-140]), np.array([63]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        # phi         = - 81.097
        # U       = np.sin(phi/180.*np.pi)
        # V       = np.cos(phi/180.*np.pi)
        # m.quiver(xc, yc, U, V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # m.quiver(xc, yc, -U, -V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # 
        # xc, yc      = m(np.array([-146]), np.array([65]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        # phi         = 75.8076
        # U       = np.sin(phi/180.*np.pi)
        # V       = np.cos(phi/180.*np.pi)
        # m.quiver(xc, yc, U, V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # m.quiver(xc, yc, -U, -V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # 
        # xc, yc      = m(np.array([-153]), np.array([64]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        # phi         = 53.1896
        # U       = np.sin(phi/180.*np.pi)
        # V       = np.cos(phi/180.*np.pi)
        # m.quiver(xc, yc, U, V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # m.quiver(xc, yc, -U, -V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # 
        # xc, yc      = m(np.array([-156]), np.array([62]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        # phi         = 32.1394
        # U       = np.sin(phi/180.*np.pi)
        # V       = np.cos(phi/180.*np.pi)
        # m.quiver(xc, yc, U, V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        # m.quiver(xc, yc, -U, -V, scale=10, width=.005, headaxislength=0, headlength=0, headwidth=0.5, color = 'b')
        #######################################
        
        
        def read_slab_contour(infname, depth):
            ctrlst  = []
            lonlst  = []
            latlst  = []
            with open(infname, 'rb') as fio:
                newctr  = False
                for line in fio.readlines():
                    if line.split()[0] is '>':
                        newctr  = True
                        if len(lonlst) != 0:
                            ctrlst.append([lonlst, latlst])
                        lonlst  = []
                        latlst  = []
                        z       = -float(line.split()[1])
                        if z == depth:
                            skipflag    = False
                        else:
                            skipflag    = True
                        continue
                    if skipflag:
                        continue
                    lonlst.append(float(line.split()[0]))
                    latlst.append(float(line.split()[1]))
            return ctrlst
        dlst    = [40., 60., 80., 100.]
        # dlst    = [100.]
        
                # m.plot(xslb, yslb,  '--', lw = 3, color='white')
        
        ###    
        arr             = np.loadtxt('SlabE325.dat')
        lonslb          = arr[:, 0]
        latslb          = arr[:, 1]
        depthslb        = -arr[:, 2]
        for depth in dlst:
            # index           = (depthslb > (depth - .05))*(depthslb < (depth + .05))
            index           = (depthslb == depth)
            lonslb2         = lonslb[index]
            latslb2         = latslb[index]
            indsort         = lonslb2.argsort()
            lonslb2         = lonslb2[indsort]
            latslb2         = latslb2[indsort]
            xslb, yslb      = m(lonslb2, latslb2)
            # m.plot(xslb, yslb,  '-', lw = 5, color='black')
            m.plot(xslb, yslb,  '-', lw = 3, color='red')
        
        
        
        # xc, yc      = m(np.array([-140]), np.array([63]))
        # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
        
        # xc, yc      = m(np.array([-146, -142]), np.array([58, 64]))
        # m.plot(xc, yc,'k', lw = 5, color='black')
        # m.plot(xc, yc,'k', lw = 3, color='white')
        # 
        # xc, yc      = m(np.array([-147, -159]), np.array([56, 62]))
        # m.plot(xc, yc,'k', lw = 5, color='black')
        # m.plot(xc, yc,'k', lw = 3, color='white')
        # plot_fault_lines(m, 'AK_Faults.txt')
        #
        import shapefile
        shapefname  = '/home/lili/data_marin/map_data/volcano_locs/SDE_GLB_VOLC.shp'
        shplst      = shapefile.Reader(shapefname)
        for rec in shplst.records():
            lon_vol = rec[4]
            lat_vol = rec[3]
            xvol, yvol            = m(lon_vol, lat_vol)
            m.plot(xvol, yvol, '^', mfc='white', mec='k', ms=10)
        #
        #############################
        yakutat_slb_dat     = np.loadtxt('YAK_extent.txt')
        yatlons             = yakutat_slb_dat[:, 0]
        yatlats             = yakutat_slb_dat[:, 1]
        xyat, yyat          = m(yatlons, yatlats)
        m.plot(xyat, yyat, '-', lw = 5, color='black')
        m.plot(xyat, yyat, '-', lw = 3, color='white')
        #############################
        plot_fault_lines(m, 'AK_Faults.txt', color='blue')
        
        xc, yc      = m(np.array([-153]), np.array([66.1]))
        m.plot(xc, yc,'s', ms = 10, markeredgecolor='black', markerfacecolor='cyan')
        xc, yc      = m(np.array([-138]), np.array([60.3]))
        m.plot(xc, yc,'s', ms = 10, markeredgecolor='black', markerfacecolor='cyan')
        
        xc, yc      = m(np.array([-150]), np.array([62.]))
        m.plot(xc, yc,'*', ms = 20, markeredgecolor='black', markerfacecolor='yellow')
        xc, yc      = m(np.array([-151]), np.array([64.]))
        m.plot(xc, yc,'*', ms = 20, markeredgecolor='black', markerfacecolor='yellow')
        
        if showfig:
            plt.savefig('alaska_sta.png')
            # plt.show()
        return
    
    
            
        
        
        
    
    