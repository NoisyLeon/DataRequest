import pyasdf



class obspyDMTASDF(pyasdf.ASDFDataSet):
    """ An object to for downloaded data manipulation based on ASDF database
    """
    
    def get_station_data(self, datadir):
        
        
    # 
    # def read_stationtxt(self, stafile, source='CIEI', chans=['BHZ', 'BHE', 'BHN']):
    #     """Read txt station list 
    #     """
    #     sta_info=sta_info_default.copy()
    #     with open(stafile, 'r') as f:
    #         Sta=[]
    #         site=obspy.core.inventory.util.Site(name='01')
    #         creation_date=obspy.core.utcdatetime.UTCDateTime(0)
    #         inv=obspy.core.inventory.inventory.Inventory(networks=[], source=source)
    #         total_number_of_channels=len(chans)
    #         for lines in f.readlines():
    #             lines=lines.split()
    #             netsta=lines[0]
    #             netcode=netsta[:2]
    #             stacode=netsta[2:]
    #             if stacode[-1]=='/':
    #                 stacode=stacode[:-1]
    #                 print netcode, stacode
    #             lon=float(lines[1])
    #             lat=float(lines[2])
    #             if lat>90.:
    #                 lon=float(lines[2])
    #                 lat=float(lines[1])
    #             netsta=netcode+'.'+stacode
    #             if Sta.__contains__(netsta):
    #                 index=Sta.index(netsta)
    #                 if abs(self[index].lon-lon) >0.01 and abs(self[index].lat-lat) >0.01:
    #                     raise ValueError('Incompatible Station Location:' + netsta+' in Station List!')
    #                 else:
    #                     print 'Warning: Repeated Station:' +netsta+' in Station List!'
    #                     continue
    #             channels=[]
    #             if lon>180.: lon-=360.
    #             for chan in chans:
    #                 channel=obspy.core.inventory.channel.Channel(code=chan, location_code='01', latitude=lat, longitude=lon,
    #                         elevation=0.0, depth=0.0)
    #                 channels.append(channel)
    #             station=obspy.core.inventory.station.Station(code=stacode, latitude=lat, longitude=lon, elevation=0.0,
    #                     site=site, channels=channels, total_number_of_channels = total_number_of_channels, creation_date = creation_date)
    #             network=obspy.core.inventory.network.Network(code=netcode, stations=[station])
    #             networks=[network]
    #             inv+=obspy.core.inventory.inventory.Inventory(networks=networks, source=source)
    #     print 'Writing obspy inventory to ASDF dataset'
    #     self.add_stationxml(inv)
    #     print 'End writing obspy inventory to ASDF dataset'
    #     return
    
    
    
    # 
    # def print_info(self):
    #     """
    #     Print information of the dataset.
    #     =================================================================================================================
    #     Version History:
    #         Dec 8th, 2016   - first version
    #     =================================================================================================================
    #     """
    #     outstr  = '============================================================ Earthquake Database ===========================================================\n'
    #     outstr+=self.__str__()+'\n'
    #     outstr += '--------------------------------------------------------- Surface wave auxiliary Data ------------------------------------------------------\n'
    #     # # if 'NoiseXcorr' in self.auxiliary_data.list():
    #     # #     outstr      += 'NoiseXcorr              - Cross-correlation seismogram\n'
    #     # # if 'StaInfo' in self.auxiliary_data.list():
    #     # #     outstr      += 'StaInfo                 - Auxiliary station information\n'
    #     if 'DISPbasic1' in self.auxiliary_data.list():
    #         outstr      += 'DISPbasic1              - Basic dispersion curve, no jump correction\n'
    #     if 'DISPbasic2' in self.auxiliary_data.list():
    #         outstr      += 'DISPbasic2              - Basic dispersion curve, with jump correction\n'
    #     if 'DISPpmf1' in self.auxiliary_data.list():
    #         outstr      += 'DISPpmf1                - PMF dispersion curve, no jump correction\n'
    #     if 'DISPpmf2' in self.auxiliary_data.list():
    #         outstr      += 'DISPpmf2                - PMF dispersion curve, with jump correction\n'
    #     if 'DISPbasic1interp' in self.auxiliary_data.list():
    #         outstr      += 'DISPbasic1interp        - Interpolated DISPbasic1\n'
    #     if 'DISPbasic2interp' in self.auxiliary_data.list():
    #         outstr      += 'DISPbasic2interp        - Interpolated DISPbasic2\n'
    #     if 'DISPpmf1interp' in self.auxiliary_data.list():
    #         outstr      += 'DISPpmf1interp          - Interpolated DISPpmf1\n'
    #     if 'DISPpmf2interp' in self.auxiliary_data.list():
    #         outstr      += 'DISPpmf2interp          - Interpolated DISPpmf2\n'
    #     if 'FieldDISPbasic1interp' in self.auxiliary_data.list():
    #         outstr      += 'FieldDISPbasic1interp   - Field data of DISPbasic1\n'
    #     if 'FieldDISPbasic2interp' in self.auxiliary_data.list():
    #         outstr      += 'FieldDISPbasic2interp   - Field data of DISPbasic2\n'
    #     if 'FieldDISPpmf1interp' in self.auxiliary_data.list():
    #         outstr      += 'FieldDISPpmf1interp     - Field data of DISPpmf1\n'
    #     if 'FieldDISPpmf2interp' in self.auxiliary_data.list():
    #         outstr      += 'FieldDISPpmf2interp     - Field data of DISPpmf2\n'
    #     outstr += '------------------------------------------------------ Receiver function auxiliary Data ----------------------------------------------------\n'
    #     if 'RefR' in self.auxiliary_data.list():
    #         outstr      += 'RefR                    - Radial receiver function\n'
    #     if 'RefRHS' in self.auxiliary_data.list():
    #         outstr      += 'RefRHS                  - Harmonic stripping results of radial receiver function\n'
    #     if 'RefRmoveout' in self.auxiliary_data.list():
    #         outstr      += 'RefRmoveout             - Move out of radial receiver function\n'
    #     if 'RefRscaled' in self.auxiliary_data.list():
    #         outstr      += 'RefRscaled              - Scaled radial receiver function\n'
    #     if 'RefRstreback' in self.auxiliary_data.list():
    #         outstr      += 'RefRstreback            - Stretch back of radial receiver function\n'
    #     outstr += '============================================================================================================================================\n'
    #     print outstr
    #     return
    # 
    # def get_events(self, startdate, enddate, add2dbase=True, gcmt=False, Mmin=5.5, Mmax=None, minlatitude=None, maxlatitude=None, minlongitude=None, maxlongitude=None,
    #         latitude=None, longitude=None, minradius=None, maxradius=None, mindepth=None, maxdepth=None, magnitudetype=None):
    #     """Get earthquake catalog from IRIS server
    #     =======================================================================================================
    #     Input Parameters:
    #     startdate, enddata  - start/end date for searching
    #     Mmin, Mmax          - minimum/maximum magnitude for searching                
    #     minlatitude         - Limit to events with a latitude larger than the specified minimum.
    #     maxlatitude         - Limit to events with a latitude smaller than the specified maximum.
    #     minlongitude        - Limit to events with a longitude larger than the specified minimum.
    #     maxlongitude        - Limit to events with a longitude smaller than the specified maximum.
    #     latitude            - Specify the latitude to be used for a radius search.
    #     longitude           - Specify the longitude to the used for a radius search.
    #     minradius           - Limit to events within the specified minimum number of degrees from the
    #                             geographic point defined by the latitude and longitude parameters.
    #     maxradius           - Limit to events within the specified maximum number of degrees from the
    #                             geographic point defined by the latitude and longitude parameters.
    #     mindepth            - Limit to events with depth, in kilometers, larger than the specified minimum.
    #     maxdepth            - Limit to events with depth, in kilometers, smaller than the specified maximum.
    #     magnitudetype       - Specify a magnitude type to use for testing the minimum and maximum limits.
    #     =======================================================================================================
    #     """
    #     starttime=obspy.core.utcdatetime.UTCDateTime(startdate)
    #     endtime=obspy.core.utcdatetime.UTCDateTime(enddate)
    #     if not gcmt:
    #         client=Client('IRIS')
    #         try:
    #             catISC = client.get_events(starttime=starttime, endtime=endtime, minmagnitude=Mmin, maxmagnitude=Mmax, catalog='ISC',
    #                 minlatitude=minlatitude, maxlatitude=maxlatitude, minlongitude=minlongitude, maxlongitude=maxlongitude,
    #                 latitude=latitude, longitude=longitude, minradius=minradius, maxradius=maxradius, mindepth=mindepth,
    #                 maxdepth=maxdepth, magnitudetype=magnitudetype)
    #             endtimeISC=catISC[0].origins[0].time
    #         except:
    #             catISC=obspy.core.event.Catalog()
    #             endtimeISC=starttime
    #         if endtime.julday-endtimeISC.julday >1:
    #             try:
    #                 catPDE = client.get_events(starttime=endtimeISC, endtime=endtime, minmagnitude=Mmin, maxmagnitude=Mmax, catalog='NEIC PDE',
    #                     minlatitude=minlatitude, maxlatitude=maxlatitude, minlongitude=minlongitude, maxlongitude=maxlongitude,
    #                     latitude=latitude, longitude=longitude, minradius=minradius, maxradius=maxradius, mindepth=mindepth,
    #                     maxdepth=maxdepth, magnitudetype=magnitudetype)
    #                 catalog=catISC+catPDE
    #             except: catalog=catISC
    #         else: catalog=catISC
    #         outcatalog=obspy.core.event.Catalog()
    #         # check magnitude
    #         for event in catalog:
    #             if event.magnitudes[0].mag < Mmin: continue
    #             outcatalog.append(event)
    #     else:
    #         gcmt_url_old='http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/jan76_dec13.ndk'
    #         gcmt_new='http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/NEW_MONTHLY'
    #         if starttime.year < 2005:
    #             cat_old=obspy.read_events(gcmt_url_old)
    #             outcatalog=cat_old.filter("magnitude >= %g" %Mmin, "time >= %s" %str(starttime), "time <= %s" %str(endtime) )
    #             if Mmax!=None: cat_old=cat_old.filter("magnitude <= %g" %Mmax)
    #             if maxlongitude!=None: cat_old=cat_old.filter("longitude <= %g" %maxlongitude)
    #             if minlongitude!=None: cat_old=cat_old.filter("longitude >= %g" %minlongitude)
    #             if maxlatitude!=None: cat_old=cat_old.filter("latitude <= %g" %maxlatitude)
    #             if minlatitude!=None: cat_old=cat_old.filter("latitude >= %g" %minlatitude)
    #             if maxdepth!=None: cat_old=cat_old.filter("depth <= %g" %(maxdepth*1000.))
    #             if mindepth!=None: cat_old=cat_old.filter("depth >= %g" %(mindepth*1000.))
    #             temp_stime=obspy.core.utcdatetime.UTCDateTime('2014-01-01')
    #             outcatalog=cat_old
    #         else:
    #             outcatalog=obspy.core.event.Catalog()
    #             temp_stime=copy.deepcopy(starttime); temp_stime.day=1
    #         while (temp_stime < endtime):
    #             year=temp_stime.year; month=temp_stime.month
    #             yearstr=str(int(year))[2:]; monstr=monthdict[month]; monstr=monstr.lower()
    #             if year==2005 and month==6: monstr='june'
    #             if year==2005 and month==7: monstr='july'
    #             if year==2005 and month==9: monstr='sept'
    #             gcmt_url_new=gcmt_new+'/'+str(int(year))+'/'+monstr+yearstr+'.ndk'
    #             print gcmt_url_new
    #             try: cat_new=obspy.read_events(gcmt_url_new)
    #             except: break
    #             cat_new=cat_new.filter("magnitude >= %g" %Mmin, "time >= %s" %str(starttime), "time <= %s" %str(endtime) )
    #             if Mmax!=None: cat_new=cat_new.filter("magnitude <= %g" %Mmax)
    #             if maxlongitude!=None: cat_new=cat_new.filter("longitude <= %g" %maxlongitude)
    #             if minlongitude!=None: cat_new=cat_new.filter("longitude >= %g" %minlongitude)
    #             if maxlatitude!=None: cat_new=cat_new.filter("latitude <= %g" %maxlatitude)
    #             if minlatitude!=None: cat_new=cat_new.filter("latitude >= %g" %minlatitude)
    #             if maxdepth!=None: cat_new=cat_new.filter("depth <= %g" %(maxdepth*1000.))
    #             if mindepth!=None: cat_new=cat_new.filter("depth >= %g" %(mindepth*1000.))
    #             outcatalog+=cat_new
    #             try: temp_stime.month+=1
    #             except: temp_stime.year+=1; temp_stime.month=1
    #     if add2dbase: self.add_quakeml(outcatalog)
    #     else: return outcatalog
    #     return
    
    
    # 
    # def read_sac(self, datadir):
    #     """This function is a scratch for reading a specific datasets, DO NOT use this function!
    #     """
    #     L=len(self.events)
    #     evnumb=0
    #     import glob
    #     for event in self.events:
    #         event_id=event.resource_id.id.split('=')[-1]
    #         magnitude=event.magnitudes[0].mag; Mtype=event.magnitudes[0].magnitude_type
    #         event_descrip=event.event_descriptions[0].text+', '+event.event_descriptions[0].type
    #         evnumb+=1
    #         print '================================= Getting surface wave data ==================================='
    #         print 'Event ' + str(evnumb)+' : '+event_descrip+', '+Mtype+' = '+str(magnitude) 
    #         st=obspy.Stream()
    #         otime=event.origins[0].time
    #         evlo=event.origins[0].longitude; evla=event.origins[0].latitude
    #         tag='surf_ev_%05d' %evnumb
    #         # if lon0!=None and lat0!=None:
    #         #     dist, az, baz=obspy.geodetics.gps2dist_azimuth(evla, evlo, lat0, lon0) # distance is in m
    #         #     dist=dist/1000.
    #         #     starttime=otime+dist/vmax; endtime=otime+dist/vmin
    #         #     commontime=True
    #         # else:
    #         #     commontime=False
    #         odate=str(otime.year)+'%02d' %otime.month +'%02d' %otime.day
    #         for staid in self.waveforms.list():
    #             netcode, stacode=staid.split('.')
    #             print staid
    #             stla, elev, stlo=self.waveforms[staid].coordinates.values()
    #             # sta_datadir=datadir+'/'+netcode+'/'+stacode
    #             sta_datadir=datadir+'/'+netcode+'/'+stacode
    #             sacpfx=sta_datadir+'/'+stacode+'.'+odate
    #             
    #             pzpfx='/home/lili/code/china_data/response_files/SAC_*'+netcode+'_'+stacode
    #             respfx='/home/lili/code/china_data/RESP4WeisenCUB/dbRESPCNV20131007/'+netcode+'/'+staid+'/RESP.'+staid
    #             st=obspy.Stream()
    #             for chan in ['*Z', '*E', '*N']:
    #                 sacfname = sacpfx+chan
    #                 pzfpattern  = pzpfx+'_'+chan
    #                 respfpattern= respfx+'*BH'+chan[-1]+'*'
    #                 #################
    #                 try: respfname=glob.glob(respfpattern)[0]
    #                 except: break
    #                 seedresp = {'filename': respfname,  # RESP filename
    #                 # when using Trace/Stream.simulate() the "date" parameter can
    #                 # also be omitted, and the starttime of the trace is then used.
    #                 # Units to return response in ('DIS', 'VEL' or ACC)
    #                 'units': 'VEL'
    #                 }
    #                 try: tr=obspy.read(sacfname)[0]
    #                 except: break
    #                 tr.detrend()
    #                 tr.stats.channel='BH'+chan[-1]
    #                 tr.simulate(paz_remove=None, pre_filt=(0.001, 0.005, 1, 100.0), seedresp=seedresp)
    #                 ################
    #                 # try: pzfname = glob.glob(pzfpattern)[0]
    #                 # except: break
    #                 # try: tr=obspy.read(sacfname)[0]
    #                 # except: break
    #                 # obspy.io.sac.sacpz.attach_paz(tr, pzfname)
    #                 # tr.decimate(10)
    #                 # tr.detrend()
    #                 # tr.simulate(paz_remove=tr.stats.paz, pre_filt=(0.001, 0.005, 1, 100.0))
    #                 st.append(tr)
    #             self.add_waveforms(st, event_id=event_id, tag=tag)    
    # 
    # def _get_basemap(self, projection='lambert', geopolygons=None, resolution='i'):
    #     """Get basemap for plotting results
    #     """
    #     # fig=plt.figure(num=None, figsize=(12, 12), dpi=80, facecolor='w', edgecolor='k')
    #     lat_centre = (self.maxlat+self.minlat)/2.0
    #     lon_centre = (self.maxlon+self.minlon)/2.0
    #     if projection=='merc':
    #         m=Basemap(projection='merc', llcrnrlat=self.minlat-5., urcrnrlat=self.maxlat+5., llcrnrlon=self.minlon-5.,
    #                   urcrnrlon=self.maxlon+5., lat_ts=20, resolution=resolution)
    #         m.drawparallels(np.arange(-80.0,80.0,5.0), labels=[1,0,0,1])
    #         m.drawmeridians(np.arange(-170.0,170.0,5.0), labels=[1,0,0,1])
    #         m.drawstates(color='g', linewidth=2.)
    #     elif projection=='global':
    #         m=Basemap(projection='ortho',lon_0=lon_centre, lat_0=lat_centre, resolution=resolution)
    #         m.drawparallels(np.arange(-80.0,80.0,10.0), labels=[1,0,0,1])
    #         m.drawmeridians(np.arange(-170.0,170.0,10.0), labels=[1,0,0,1])
    #     
    #     elif projection=='regional_ortho':
    #         m1 = Basemap(projection='ortho', lon_0=self.minlon, lat_0=self.minlat, resolution='l')
    #         m = Basemap(projection='ortho', lon_0=self.minlon, lat_0=self.minlat, resolution=resolution,\
    #             llcrnrx=0., llcrnry=0., urcrnrx=m1.urcrnrx/mapfactor, urcrnry=m1.urcrnry/3.5)
    #         m.drawparallels(np.arange(-80.0,80.0,10.0), labels=[1,0,0,0],  linewidth=2,  fontsize=20)
    #         m.drawmeridians(np.arange(-170.0,170.0,10.0),  linewidth=2)
    #     elif projection=='lambert':
    #         distEW, az, baz=obspy.geodetics.gps2dist_azimuth(self.minlat, self.minlon,
    #                             self.minlat, self.maxlon) # distance is in m
    #         distNS, az, baz=obspy.geodetics.gps2dist_azimuth(self.minlat, self.minlon,
    #                             self.maxlat+2., self.minlon) # distance is in m
    #         m = Basemap(width=distEW, height=distNS, rsphere=(6378137.00,6356752.3142), resolution='l', projection='lcc',\
    #             lat_1=self.minlat, lat_2=self.maxlat, lon_0=lon_centre, lat_0=lat_centre+1)
    #         m.drawparallels(np.arange(-80.0,80.0,10.0), linewidth=1, dashes=[2,2], labels=[1,1,0,0], fontsize=15)
    #         m.drawmeridians(np.arange(-170.0,170.0,10.0), linewidth=1, dashes=[2,2], labels=[0,0,1,0], fontsize=15)
    #     m.drawcoastlines(linewidth=1.0)
    #     m.drawcountries(linewidth=1.)
    #     m.fillcontinents(lake_color='#99ffff',zorder=0.2)
    #     m.drawmapboundary(fill_color="white")
    #     m.drawstates()
    #     try: geopolygons.PlotPolygon(inbasemap=m)
    #     except: pass
    #     return m
    # 
    # def plot_events(self, gcmt=False, projection='lambert', valuetype='depth', geopolygons=None, showfig=True, vmin=None, vmax=None):
    #     if gcmt: from obspy.imaging.beachball import beach; ax = plt.gca()
    #     evlons=np.array([])
    #     evlats=np.array([])
    #     values=np.array([])
    #     focmecs=[]
    #     for event in self.events:
    #         event_id=event.resource_id.id.split('=')[-1]
    #         magnitude=event.magnitudes[0].mag; Mtype=event.magnitudes[0].magnitude_type
    #         otime=event.origins[0].time
    #         evlo=event.origins[0].longitude; evla=event.origins[0].latitude; evdp=event.origins[0].depth/1000.
    #         if evlo > -80.: continue
    #         evlons=np.append(evlons, evlo); evlats = np.append(evlats, evla);
    #         if valuetype=='depth': values=np.append(values, evdp)
    #         elif valuetype=='mag': values=np.append(values, magnitude)
    #         if gcmt:
    #             mtensor=event.focal_mechanisms[0].moment_tensor.tensor
    #             mt=[mtensor.m_rr, mtensor.m_tt, mtensor.m_pp, mtensor.m_rt, mtensor.m_rp, mtensor.m_tp]
    #             # nodalP=event.focal_mechanisms[0].nodal_planes.values()[1]
    #             # mt=[nodalP.strike, nodalP.dip, nodalP.rake]
    #             focmecs.append(mt)
    #     self.minlat=evlats.min()-1.; self.maxlat=evlats.max()+1.
    #     self.minlon=evlons.min()-1.; self.maxlon=evlons.max()+1.
    #     # self.minlat=15; self.maxlat=50
    #     # self.minlon=95; self.maxlon=128
    #     m=self._get_basemap(projection=projection, geopolygons=geopolygons)
    #     import pycpt
    #     cmap=pycpt.load.gmtColormap('./GMT_panoply.cpt')
    #     # cmap =discrete_cmap(int((vmax-vmin)/0.1)+1, cmap)
    #     x, y=m(evlons, evlats)
    #     if vmax==None and vmin==None: vmax=values.max(); vmin=values.min()
    #     if gcmt:
    #         for i in xrange(len(focmecs)):
    #             value=values[i]
    #             rgbcolor=cmap( (value-vmin)/(vmax-vmin) )
    #             b = beach(focmecs[i], xy=(x[i], y[i]), width=100000, linewidth=1, facecolor=rgbcolor)
    #             b.set_zorder(10)
    #             ax.add_collection(b)
    #             # ax.annotate(str(i), (x[i]+50000, y[i]+50000))
    #         im=m.scatter(x, y, marker='o', s=1, c=values, cmap=cmap, vmin=vmin, vmax=vmax)
    #         cb = m.colorbar(im, "bottom", size="3%", pad='2%')
    #         cb.set_label(valuetype, fontsize=20)
    #     else:
    #         if values.size!=0:
    #             im=m.scatter(x, y, marker='o', s=300, c=values, cmap=cmap, vmin=vmin, vmax=vmax)
    #             cb = m.colorbar(im, "bottom", size="3%", pad='2%')
    #         else: m.plot(x,y,'o')
    #     if gcmt: stime=self.events[0].origins[0].time; etime=self.events[-1].origins[0].time
    #     else: etime=self.events[0].origins[0].time; stime=self.events[-1].origins[0].time
    #     plt.suptitle('Number of event: '+str(len(self.events))+' time range: '+str(stime)+' - '+str(etime), fontsize=20 )
    #     if showfig: plt.show()
    #     return   
    # 
    # def get_stations(self, startdate=None, enddate=None,  network=None, station=None, location=None, channel=None,
    #         minlatitude=None, maxlatitude=None, minlongitude=None, maxlongitude=None, latitude=None, longitude=None, minradius=None, maxradius=None):
    #     """Get station inventory from IRIS server
    #     =======================================================================================================
    #     Input Parameters:
    #     startdate, enddata  - start/end date for searching
    #     network             - Select one or more network codes.
    #                             Can be SEED network codes or data center defined codes.
    #                                 Multiple codes are comma-separated (e.g. "IU,TA").
    #     station             - Select one or more SEED station codes.
    #                             Multiple codes are comma-separated (e.g. "ANMO,PFO").
    #     location            - Select one or more SEED location identifiers.
    #                             Multiple identifiers are comma-separated (e.g. "00,01").
    #                             As a special case ?--? (two dashes) will be translated to a string of two space
    #                             characters to match blank location IDs.
    #     channel             - Select one or more SEED channel codes.
    #                             Multiple codes are comma-separated (e.g. "BHZ,HHZ").             
    #     minlatitude         - Limit to events with a latitude larger than the specified minimum.
    #     maxlatitude         - Limit to events with a latitude smaller than the specified maximum.
    #     minlongitude        - Limit to events with a longitude larger than the specified minimum.
    #     maxlongitude        - Limit to events with a longitude smaller than the specified maximum.
    #     latitude            - Specify the latitude to be used for a radius search.
    #     longitude           - Specify the longitude to the used for a radius search.
    #     minradius           - Limit to events within the specified minimum number of degrees from the
    #                             geographic point defined by the latitude and longitude parameters.
    #     maxradius           - Limit to events within the specified maximum number of degrees from the
    #                             geographic point defined by the latitude and longitude parameters.
    #     =======================================================================================================
    #     """
    #     try: starttime=obspy.core.utcdatetime.UTCDateTime(startdate)
    #     except: starttime=None
    #     try: endtime=obspy.core.utcdatetime.UTCDateTime(enddate)
    #     except: endtime=None
    #     client=Client('IRIS')
    #     inv = client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, channel=channel, 
    #         minlatitude=minlatitude, maxlatitude=maxlatitude, minlongitude=minlongitude, maxlongitude=maxlongitude,
    #         latitude=latitude, longitude=longitude, minradius=minradius, maxradius=maxradius, level='channel')
    #     self.add_stationxml(inv)
    #     try:
    #         self.inv+=inv
    #     except:
    #         self.inv=inv
    #     return 
    