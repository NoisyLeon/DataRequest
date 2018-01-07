# -*- coding: utf-8 -*-
"""
A python module for processing seismic data downloaded using obspyDMT

    
:Copyright:
    Author: Lili Feng
    Graduate Research Assistant
    CIEI, Department of Physics, University of Colorado Boulder
    email: lili.feng@colorado.edu
"""
import pyasdf
import numpy as np
import matplotlib.pyplot as plt
import obspy
import glob, os
from functools import partial
import multiprocessing
from pyproj import Geod

geodist             = Geod(ellps='WGS84')

class StaInfo(object):
    """
    An object contains a station information
    ===========================================
    ::: parameters :::
    stacode     - station name
    network     - network
    lon,lat     - position for station
    ===========================================
    """
    def __init__(self, stacode=None, network='', lat=None, lon=None):

        self.stacode    = stacode
        self.network    = network
        self.lon        = lon
        self.lat        = lat


class DMTASDF(pyasdf.ASDFDataSet):
    
    def copy_catalog(self):
        print('Copying catalog from ASDF to memory')
        self.cat    = self.events.copy()
        return
    
    def read_quakeml(self, inquakeml, add2dbase=False):
        self.cat    = obspy.read_events(inquakeml)
        if add2dbase:
            self.add_quakeml(self.cat)
        return
        
    def remove_resp_catalog(self, datadir, verbose=False, fs=40., startdate=None, enddate=None, rotation=True, saveEN=True):
        """
        remove response according to event catalog
        """
        evnumb              = 0
        try:
            print self.cat
        except AttributeError:
            self.copy_catalog()
        try:
            stime4resp  = obspy.core.utcdatetime.UTCDateTime(startdate)
        except:
            stime4resp  = obspy.UTCDateTime(0)
        try:
            etime4resp  = obspy.core.utcdatetime.UTCDateTime(enddate)
        except:
            etime4resp  = obspy.UTCDateTime()
        errordir    = datadir+'/error_dir'
        if not os.path.isdir(errordir):
            os.makedirs(errordir)
        for event in self.cat:
            event_id        = event.resource_id.id.split('=')[-1]
            pmag            = event.preferred_magnitude()
            magnitude       = pmag.mag
            Mtype           = pmag.magnitude_type
            event_descrip   = event.event_descriptions[0].text+', '+event.event_descriptions[0].type
            evnumb          +=1
            porigin         = event.preferred_origin()
            otime           = porigin.time
            if otime < stime4resp or otime > etime4resp:
                continue
            print('Event ' + str(evnumb)+' : '+ str(otime)+' '+ event_descrip+', '+Mtype+' = '+str(magnitude))
            evlo            = porigin.longitude
            evla            = porigin.latitude
            evdp            = porigin.depth/1000.
            subdir          = datadir+'/'+'%d%02d%02d_%02d%02d%02d.a' \
                                %(otime.year, otime.month, otime.day, otime.hour, otime.minute, otime.second)
            Ndata           = 0
            outstr          = ''
            outdir          = subdir+'/processed'
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            respdir         = subdir+'/resp'
            rawdir          = subdir+'/raw'
            for staid in self.waveforms.list():
                netcode, stacode    = staid.split('.')
                #---------------------------------------
                # file existence
                #---------------------------------------
                fnameZ              = rawdir+'/'+netcode+'.'+stacode + '..BHZ'
                fnameE              = rawdir+'/'+netcode+'.'+stacode + '..BHE'
                fnameN              = rawdir+'/'+netcode+'.'+stacode + '..BHN'
                outfnameZ           = outdir+'/'+netcode+'.'+stacode+'..BHZ'
                outfnameE           = outdir+'/'+netcode+'.'+stacode+'..BHE'
                outfnameN           = outdir+'/'+netcode+'.'+stacode+'..BHN'
                invfnameZ           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHZ'
                invfnameE           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHE'
                invfnameN           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHN'
                if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                    fnameZ          = rawdir+'/'+netcode+'.'+stacode + '.00.BHZ'
                    fnameE          = rawdir+'/'+netcode+'.'+stacode + '.00.BHE'
                    fnameN          = rawdir+'/'+netcode+'.'+stacode + '.00.BHN'
                    outfnameZ       = outdir+'/'+netcode+'.'+stacode+'.00.BHZ'
                    outfnameE       = outdir+'/'+netcode+'.'+stacode+'.00.BHE'
                    outfnameN       = outdir+'/'+netcode+'.'+stacode+'.00.BHN'
                    invfnameZ       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHZ'
                    invfnameE       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHE'
                    invfnameN       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHN'
                    if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                        fnameZ      = rawdir+'/'+netcode+'.'+stacode + '.10.BHZ'
                        fnameE      = rawdir+'/'+netcode+'.'+stacode + '.10.BHE'
                        fnameN      = rawdir+'/'+netcode+'.'+stacode + '.10.BHN'
                        outfnameZ   = outdir+'/'+netcode+'.'+stacode+'.10.BHZ'
                        outfnameE   = outdir+'/'+netcode+'.'+stacode+'.10.BHE'
                        outfnameN   = outdir+'/'+netcode+'.'+stacode+'.10.BHN'
                        invfnameZ   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHZ'
                        invfnameE   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHE'
                        invfnameN   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHN'
                        if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                            fnameZ      = rawdir+'/'+netcode+'.'+stacode + '.01.BHZ'
                            fnameE      = rawdir+'/'+netcode+'.'+stacode + '.01.BHE'
                            fnameN      = rawdir+'/'+netcode+'.'+stacode + '.01.BHN'
                            outfnameZ   = outdir+'/'+netcode+'.'+stacode+'.01.BHZ'
                            outfnameE   = outdir+'/'+netcode+'.'+stacode+'.01.BHE'
                            outfnameN   = outdir+'/'+netcode+'.'+stacode+'.01.BHN'
                            invfnameZ   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHZ'
                            invfnameE   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHE'
                            invfnameN   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHN'
                            if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                                if verbose:
                                    print('No data for: '+staid)
                                continue
                if not (os.path.isfile(invfnameZ) and os.path.isfile(invfnameE) and os.path.isfile(invfnameN)):
                    if verbose:
                        print('No resp for: '+staid)
                    continue
                # read data
                if verbose:
                    print('removing resp for: '+ staid)
                st                  = obspy.read(fnameZ)
                st                  +=obspy.read(fnameE)
                st                  +=obspy.read(fnameN)
                if len(st) != 3:
                    continue
                inv                 = obspy.read_inventory(invfnameZ, format="stationxml")
                inv                 +=obspy.read_inventory(invfnameE, format="stationxml")
                inv                 +=obspy.read_inventory(invfnameN, format="stationxml")
                # removing response
                st.attach_response(inv)
                pre_filt            = (0.04, 0.05, 20., 25.)
                st.detrend()
                st.remove_response(pre_filt=pre_filt, taper_fraction=0.1)
                st.resample(sampling_rate=fs)
                # save data
                if not rotation or saveEN:
                    tr                  = st.select(channel='BHZ')[0]
                    tr.write(outfnameZ, format='mseed')
                    tr                  = st.select(channel='BHE')[0]
                    tr.write(outfnameE, format='mseed')
                    tr                  = st.select(channel='BHN')[0]
                    tr.write(outfnameN, format='mseed')
                if rotation:
                    stla, elev, stlo    = self.waveforms[staid].coordinates.values()
                    elev                = elev/1000.
                    az, baz, dist       = geodist.inv(evlo, evla, stlo, stla)
                    dist                = dist/1000.
                    if baz<0.:
                        baz             += 360.
                    try:
                        st.rotate('NE->RT', back_azimuth=baz)
                    except ValueError:
                        try:
                            stime4trim  = obspy.UTCDateTime(0)
                            etime4trim  = obspy.UTCDateTime()
                            for tr in st:
                                if stime4trim < tr.stats.starttime:
                                    stime4trim  = tr.stats.starttime
                                if etime4trim > tr.stats.endtime:
                                    etime4trim  = tr.stats.endtime
                            if stime4trim>etime4trim:
                                print('wrong timestamp: '+ staid)
                                continue
                            st.trim(starttime=stime4trim, endtime=etime4trim)
                            st.rotate('NE->RT', back_azimuth=baz)
                        except ValueError:
                            errordir    = datadir+'/error_dir'
                            errorfile   = errordir+'/%d%02d%02d_%02d%02d%02d.log' \
                                %(otime.year, otime.month, otime.day, otime.hour, otime.minute, otime.second)
                            with open(errorfile, 'a') as fid:
                                fid.writelines(staid+'\n')
                            continue
                    tr                  = st.select(channel='BHZ')[0]
                    tr.write(outfnameZ, format='mseed')
                    fnamepfx            = outfnameZ[:-1]
                    outfnameR           = fnamepfx+'R'
                    outfnameT           = fnamepfx+'T'
                    tr                  = st.select(channel='BHR')[0]
                    tr.write(outfnameR, format='mseed')
                    tr                  = st.select(channel='BHT')[0]
                    tr.write(outfnameT, format='mseed')
                Ndata   += 1
                outstr  += staid
                outstr  += ' '
            print(str(Ndata)+' data streams are resp removed!')
            print('STATION CODE: '+outstr)
            print('-----------------------------------------------------------------------------------------------------------')
        return
    
    def remove_resp_catalog_mp(self, datadir, verbose=False, fs=40., startdate=None, enddate=None, rotation=True, saveEN=True,\
                               subsize=1000, nprocess=6):
        """
        remove response according to event catalog, parallel version
        """
        try:
            stime4resp  = obspy.core.utcdatetime.UTCDateTime(startdate)
        except:
            stime4resp  = obspy.UTCDateTime(0)
        try:
            etime4resp  = obspy.core.utcdatetime.UTCDateTime(enddate)
        except:
            etime4resp  = obspy.UTCDateTime()
        # preparing catalog list for multiprocessing
        catlst          = []
        for event in self.cat:
            catlst.append(event)
        # station list
        stalst          = []
        for staid in self.waveforms.list():
            netcode, stacode    = staid.split('.')
            stla, elev, stlo    = self.waveforms[staid].coordinates.values()
            stainfo             = StaInfo()
            stainfo.network     = netcode
            stainfo.stacode     = stacode
            stainfo.lat         = stla
            stainfo.lon         = stlo
            stalst.append(stainfo)
        errordir    = datadir+'/error_dir'
        if not os.path.isdir(errordir):
            os.makedirs(errordir)
        # multiprocessing of response removing
        if len(catlst) > subsize:
            Nsub            = int(len(catlst)/subsize)
            for isub in range(Nsub):
                print 'Subset:', isub+1,'in',Nsub,'sets'
                cresplst    = catlst[isub*subsize:(isub+1)*subsize]
                REMOVERESP  = partial(remove_resp_cat4mp, datadir=datadir, stalst=stalst, stime4resp=stime4resp, etime4resp=etime4resp,\
                                      rotation=rotation, saveEN=saveEN, verbose=verbose, fs=fs)
                pool        = multiprocessing.Pool(processes=nprocess)
                pool.map(REMOVERESP, cresplst) #make our results with a map call
                pool.close() #we are not adding any more processes
                pool.join() #tell it to wait until all threads are done before going on
            cresplst        = catlst[(isub+1)*subsize:]
            REMOVERESP      = partial(remove_resp_cat4mp, datadir=datadir, stalst=stalst, stime4resp=stime4resp, etime4resp=etime4resp,\
                                      rotation=rotation, saveEN=saveEN, verbose=verbose, fs=fs)
            pool            = multiprocessing.Pool(processes=nprocess)
            pool.map(REMOVERESP, cresplst) #make our results with a map call
            pool.close() #we are not adding any more processes
            pool.join() #tell it to wait until all threads are done before going on
        else:
            REMOVERESP      = partial(remove_resp_cat4mp, datadir=datadir, stalst=stalst, stime4resp=stime4resp, etime4resp=etime4resp,\
                                      rotation=rotation, saveEN=saveEN, verbose=verbose, fs=fs)
            pool            = multiprocessing.Pool(processes=nprocess)
            pool.map(REMOVERESP, catlst) #make our results with a map call
            pool.close() #we are not adding any more processes
            pool.join() #tell it to wait until all threads are done before going on
        return
    
            
            
    def remove_resp_glob(self, datadir, verbose=False, fs=40.):
        subdirpattern   = datadir+'/*.a'
        subdirlst       = glob.glob(subdirpattern)
        
        for subdir in subdirlst:
            outdir  = subdir+'/processed'
            print('working on: '+outdir)
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
                
            respdir = subdir+'/resp'
            rawdir  = subdir+'/raw'
            for staid in self.waveforms.list():
                netcode, stacode    = staid.split('.')
                #---------------------------------------
                # file existence
                #---------------------------------------
                fnameZ              = rawdir+'/'+netcode+'.'+stacode + '..BHZ'
                fnameE              = rawdir+'/'+netcode+'.'+stacode + '..BHE'
                fnameN              = rawdir+'/'+netcode+'.'+stacode + '..BHN'
                outfnameZ           = outdir+'/'+netcode+'.'+stacode+'..BHZ'
                outfnameE           = outdir+'/'+netcode+'.'+stacode+'..BHE'
                outfnameN           = outdir+'/'+netcode+'.'+stacode+'..BHN'
                invfnameZ           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHZ'
                invfnameE           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHE'
                invfnameN           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHN'
                if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                    fnameZ          = rawdir+'/'+netcode+'.'+stacode + '.00.BHZ'
                    fnameE          = rawdir+'/'+netcode+'.'+stacode + '.00.BHE'
                    fnameN          = rawdir+'/'+netcode+'.'+stacode + '.00.BHN'
                    outfnameZ       = outdir+'/'+netcode+'.'+stacode+'.00.BHZ'
                    outfnameE       = outdir+'/'+netcode+'.'+stacode+'.00.BHE'
                    outfnameN       = outdir+'/'+netcode+'.'+stacode+'.00.BHN'
                    invfnameZ       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHZ'
                    invfnameE       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHE'
                    invfnameN       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHN'
                    if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                        fnameZ      = rawdir+'/'+netcode+'.'+stacode + '.10.BHZ'
                        fnameE      = rawdir+'/'+netcode+'.'+stacode + '.10.BHE'
                        fnameN      = rawdir+'/'+netcode+'.'+stacode + '.10.BHN'
                        outfnameZ   = outdir+'/'+netcode+'.'+stacode+'.10.BHZ'
                        outfnameE   = outdir+'/'+netcode+'.'+stacode+'.10.BHE'
                        outfnameN   = outdir+'/'+netcode+'.'+stacode+'.10.BHN'
                        invfnameZ   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHZ'
                        invfnameE   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHE'
                        invfnameN   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHN'
                        if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                            fnameZ      = rawdir+'/'+netcode+'.'+stacode + '.01.BHZ'
                            fnameE      = rawdir+'/'+netcode+'.'+stacode + '.01.BHE'
                            fnameN      = rawdir+'/'+netcode+'.'+stacode + '.01.BHN'
                            outfnameZ   = outdir+'/'+netcode+'.'+stacode+'.01.BHZ'
                            outfnameE   = outdir+'/'+netcode+'.'+stacode+'.01.BHE'
                            outfnameN   = outdir+'/'+netcode+'.'+stacode+'.01.BHN'
                            invfnameZ   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHZ'
                            invfnameE   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHE'
                            invfnameN   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHN'
                            if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                                if verbose:
                                    print('No data for: '+staid)
                                continue
                if not (os.path.isfile(invfnameZ) and os.path.isfile(invfnameE) and os.path.isfile(invfnameN)):
                    if verbose:
                        print('No resp for: '+staid)
                    continue
                # read data
                if verbose:
                    print('removing resp for: '+ staid)
                st                  = obspy.read(fnameZ)
                st                  +=obspy.read(fnameE)
                st                  +=obspy.read(fnameN)
                if len(st) != 3:
                    continue
                inv                 = obspy.read_inventory(invfnameZ, format="stationxml")
                inv                 +=obspy.read_inventory(invfnameE, format="stationxml")
                inv                 +=obspy.read_inventory(invfnameN, format="stationxml")
                # removing response
                st.attach_response(inv)
                pre_filt            = (0.04, 0.05, 20., 25.)
                st.detrend()
                st.remove_response(pre_filt=pre_filt, taper_fraction=0.1)
                st.resample(sampling_rate=fs)
                # save data
                tr                  = st.select(channel='BHZ')[0]
                tr.write(outfnameZ, format='mseed')
                tr                  = st.select(channel='BHE')[0]
                tr.write(outfnameE, format='mseed')
                tr                  = st.select(channel='BHN')[0]
                tr.write(outfnameN, format='mseed')
        return
    
    def remove_resp_glob_mp(self, datadir, verbose=False, fs=40., subsize=1000, nprocess=6):
        subdirpattern   = datadir+'/*.a'
        subdirlst       = glob.glob(subdirpattern)[:10]
        
        if len(subdirlst) > subsize:
            Nsub            = int(len(subdirlst)/subsize)
            for isub in range(Nsub):
                print 'Subset:', isub+1,'in',Nsub,'sets'
                cresplst    = subdirlst[isub*subsize:(isub+1)*subsize]
                REMOVERESP  = partial(remove_resp_glob4mp, stalst=self.waveforms.list(), verbose=verbose, fs=fs)
                pool        = multiprocessing.Pool(processes=nprocess)
                pool.map(REMOVERESP, cresplst) #make our results with a map call
                pool.close() #we are not adding any more processes
                pool.join() #tell it to wait until all threads are done before going on
                
            cresplst        = subdirlst[(isub+1)*subsize:]
            REMOVERESP      = partial(remove_resp_glob4mp, stalst=self.waveforms.list(), verbose=verbose, fs=fs)
            pool            = multiprocessing.Pool(processes=nprocess)
            pool.map(REMOVERESP, cresplst) #make our results with a map call
            pool.close() #we are not adding any more processes
            pool.join() #tell it to wait until all threads are done before going on
        else:
            REMOVERESP      = partial(remove_resp_glob4mp, stalst=self.waveforms.list(), verbose=verbose, fs=fs)
            pool            = multiprocessing.Pool(processes=nprocess)
            pool.map(REMOVERESP, subdirlst) #make our results with a map call
            pool.close() #we are not adding any more processes
            pool.join() #tell it to wait until all threads are done before going on
        return
    
    
def remove_resp_glob4mp(subdir, stalst, verbose, fs):
    outdir  = subdir+'/processed'
    print('working on: '+outdir)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    respdir = subdir+'/resp'
    rawdir  = subdir+'/raw'
    for staid in stalst:
        netcode, stacode    = staid.split('.')
        #---------------------------------------
        # file existence
        #---------------------------------------
        fnameZ              = rawdir+'/'+netcode+'.'+stacode + '..BHZ'
        fnameE              = rawdir+'/'+netcode+'.'+stacode + '..BHE'
        fnameN              = rawdir+'/'+netcode+'.'+stacode + '..BHN'
        outfnameZ           = outdir+'/'+netcode+'.'+stacode+'..BHZ'
        outfnameE           = outdir+'/'+netcode+'.'+stacode+'..BHE'
        outfnameN           = outdir+'/'+netcode+'.'+stacode+'..BHN'
        invfnameZ           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHZ'
        invfnameE           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHE'
        invfnameN           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHN'
        if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
            fnameZ          = rawdir+'/'+netcode+'.'+stacode + '.00.BHZ'
            fnameE          = rawdir+'/'+netcode+'.'+stacode + '.00.BHE'
            fnameN          = rawdir+'/'+netcode+'.'+stacode + '.00.BHN'
            outfnameZ       = outdir+'/'+netcode+'.'+stacode+'.00.BHZ'
            outfnameE       = outdir+'/'+netcode+'.'+stacode+'.00.BHE'
            outfnameN       = outdir+'/'+netcode+'.'+stacode+'.00.BHN'
            invfnameZ       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHZ'
            invfnameE       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHE'
            invfnameN       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHN'
            if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                fnameZ      = rawdir+'/'+netcode+'.'+stacode + '.10.BHZ'
                fnameE      = rawdir+'/'+netcode+'.'+stacode + '.10.BHE'
                fnameN      = rawdir+'/'+netcode+'.'+stacode + '.10.BHN'
                outfnameZ   = outdir+'/'+netcode+'.'+stacode+'.10.BHZ'
                outfnameE   = outdir+'/'+netcode+'.'+stacode+'.10.BHE'
                outfnameN   = outdir+'/'+netcode+'.'+stacode+'.10.BHN'
                invfnameZ   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHZ'
                invfnameE   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHE'
                invfnameN   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHN'
                if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                    fnameZ      = rawdir+'/'+netcode+'.'+stacode + '.01.BHZ'
                    fnameE      = rawdir+'/'+netcode+'.'+stacode + '.01.BHE'
                    fnameN      = rawdir+'/'+netcode+'.'+stacode + '.01.BHN'
                    outfnameZ   = outdir+'/'+netcode+'.'+stacode+'.01.BHZ'
                    outfnameE   = outdir+'/'+netcode+'.'+stacode+'.01.BHE'
                    outfnameN   = outdir+'/'+netcode+'.'+stacode+'.01.BHN'
                    invfnameZ   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHZ'
                    invfnameE   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHE'
                    invfnameN   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHN'
                    if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                        if verbose:
                            print('No data for: '+staid)
                        continue
        if not (os.path.isfile(invfnameZ) and os.path.isfile(invfnameE) and os.path.isfile(invfnameN)):
            if verbose:
                print('No resp for: '+staid)
            continue
        # read data
        if verbose:
            print('removing resp for: '+ staid)
        st                  = obspy.read(fnameZ)
        st                  +=obspy.read(fnameE)
        st                  +=obspy.read(fnameN)
        if len(st) != 3:
            continue
        inv                 = obspy.read_inventory(invfnameZ, format="stationxml")
        inv                 +=obspy.read_inventory(invfnameE, format="stationxml")
        inv                 +=obspy.read_inventory(invfnameN, format="stationxml")
        # removing response
        st.attach_response(inv)
        pre_filt            = (0.04, 0.05, 20., 25.)
        st.detrend()
        st.remove_response(pre_filt=pre_filt, taper_fraction=0.1)
        st.resample(sampling_rate=fs)
        # save data
        tr                  = st.select(channel='BHZ')[0]
        tr.write(outfnameZ, format='mseed')
        tr                  = st.select(channel='BHE')[0]
        tr.write(outfnameE, format='mseed')
        tr                  = st.select(channel='BHN')[0]
        tr.write(outfnameN, format='mseed')
    return


def remove_resp_cat4mp(event, datadir, stalst, stime4resp, etime4resp, rotation, saveEN, verbose, fs):
    event_id        = event.resource_id.id.split('=')[-1]
    pmag            = event.preferred_magnitude()
    magnitude       = pmag.mag
    Mtype           = pmag.magnitude_type
    event_descrip   = event.event_descriptions[0].text+', '+event.event_descriptions[0].type
    porigin         = event.preferred_origin()
    otime           = porigin.time
    if otime < stime4resp or otime > etime4resp:
        print('skip ::: event : '+ str(otime)+' '+ event_descrip+', '+Mtype+' = '+str(magnitude))
        return
    evlo            = porigin.longitude
    evla            = porigin.latitude
    evdp            = porigin.depth/1000.
    subdir          = datadir+'/'+'%d%02d%02d_%02d%02d%02d.a' \
                        %(otime.year, otime.month, otime.day, otime.hour, otime.minute, otime.second)
    Ndata           = 0
    outstr          = ''
    outdir          = subdir+'/processed'
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    respdir         = subdir+'/resp'
    rawdir          = subdir+'/raw'
    for station in stalst:
        netcode             = station.network
        stacode             = station.stacode
        staid               = netcode+'.'+stacode
        #---------------------------------------
        # file existence
        #---------------------------------------
        fnameZ              = rawdir+'/'+netcode+'.'+stacode + '..BHZ'
        fnameE              = rawdir+'/'+netcode+'.'+stacode + '..BHE'
        fnameN              = rawdir+'/'+netcode+'.'+stacode + '..BHN'
        outfnameZ           = outdir+'/'+netcode+'.'+stacode+'..BHZ'
        outfnameE           = outdir+'/'+netcode+'.'+stacode+'..BHE'
        outfnameN           = outdir+'/'+netcode+'.'+stacode+'..BHN'
        invfnameZ           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHZ'
        invfnameE           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHE'
        invfnameN           = respdir+'/STXML.'+netcode+'.'+stacode + '..BHN'
        if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
            fnameZ          = rawdir+'/'+netcode+'.'+stacode + '.00.BHZ'
            fnameE          = rawdir+'/'+netcode+'.'+stacode + '.00.BHE'
            fnameN          = rawdir+'/'+netcode+'.'+stacode + '.00.BHN'
            outfnameZ       = outdir+'/'+netcode+'.'+stacode+'.00.BHZ'
            outfnameE       = outdir+'/'+netcode+'.'+stacode+'.00.BHE'
            outfnameN       = outdir+'/'+netcode+'.'+stacode+'.00.BHN'
            invfnameZ       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHZ'
            invfnameE       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHE'
            invfnameN       = respdir+'/STXML.'+netcode+'.'+stacode + '.00.BHN'
            if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                fnameZ      = rawdir+'/'+netcode+'.'+stacode + '.10.BHZ'
                fnameE      = rawdir+'/'+netcode+'.'+stacode + '.10.BHE'
                fnameN      = rawdir+'/'+netcode+'.'+stacode + '.10.BHN'
                outfnameZ   = outdir+'/'+netcode+'.'+stacode+'.10.BHZ'
                outfnameE   = outdir+'/'+netcode+'.'+stacode+'.10.BHE'
                outfnameN   = outdir+'/'+netcode+'.'+stacode+'.10.BHN'
                invfnameZ   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHZ'
                invfnameE   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHE'
                invfnameN   = respdir+'/STXML.'+netcode+'.'+stacode + '.10.BHN'
                if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                    fnameZ      = rawdir+'/'+netcode+'.'+stacode + '.01.BHZ'
                    fnameE      = rawdir+'/'+netcode+'.'+stacode + '.01.BHE'
                    fnameN      = rawdir+'/'+netcode+'.'+stacode + '.01.BHN'
                    outfnameZ   = outdir+'/'+netcode+'.'+stacode+'.01.BHZ'
                    outfnameE   = outdir+'/'+netcode+'.'+stacode+'.01.BHE'
                    outfnameN   = outdir+'/'+netcode+'.'+stacode+'.01.BHN'
                    invfnameZ   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHZ'
                    invfnameE   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHE'
                    invfnameN   = respdir+'/STXML.'+netcode+'.'+stacode + '.01.BHN'
                    if not (os.path.isfile(fnameZ) and os.path.isfile(fnameE) and os.path.isfile(fnameN)):
                        continue
        if not (os.path.isfile(invfnameZ) and os.path.isfile(invfnameE) and os.path.isfile(invfnameN)):
            continue
        # read data
        st                  = obspy.read(fnameZ)
        st                  +=obspy.read(fnameE)
        st                  +=obspy.read(fnameN)
        if len(st) != 3:
            continue
        inv                 = obspy.read_inventory(invfnameZ, format="stationxml")
        inv                 +=obspy.read_inventory(invfnameE, format="stationxml")
        inv                 +=obspy.read_inventory(invfnameN, format="stationxml")
        # removing response
        st.attach_response(inv)
        pre_filt            = (0.04, 0.05, 20., 25.)
        st.detrend()
        st.remove_response(pre_filt=pre_filt, taper_fraction=0.1)
        st.resample(sampling_rate=fs)
        # save data
        if not rotation or saveEN:
            tr                  = st.select(channel='BHZ')[0]
            tr.write(outfnameZ, format='mseed')
            tr                  = st.select(channel='BHE')[0]
            tr.write(outfnameE, format='mseed')
            tr                  = st.select(channel='BHN')[0]
            tr.write(outfnameN, format='mseed')
        if rotation:
            stla                = station.lat
            stlo                = station.lon
            az, baz, dist       = geodist.inv(evlo, evla, stlo, stla)
            dist                = dist/1000.
            if baz<0.:
                baz             += 360.
            try:
                st.rotate('NE->RT', back_azimuth=baz)
            except ValueError:
                try:
                    stime4trim  = obspy.UTCDateTime(0)
                    etime4trim  = obspy.UTCDateTime()
                    for tr in st:
                        if stime4trim < tr.stats.starttime:
                            stime4trim  = tr.stats.starttime
                        if etime4trim > tr.stats.endtime:
                            etime4trim  = tr.stats.endtime
                    st.trim(starttime=stime4trim, endtime=etime4trim)
                    st.rotate('NE->RT', back_azimuth=baz)
                except ValueError:
                    errordir    = datadir+'/error_dir'
                    errorfile   = errordir+'/%d%02d%02d_%02d%02d%02d.log' \
                        %(otime.year, otime.month, otime.day, otime.hour, otime.minute, otime.second)
                    with open(errorfile, 'a') as fid:
                        fid.writelines(staid+'\n')
                    continue
            tr                  = st.select(channel='BHZ')[0]
            tr.write(outfnameZ, format='mseed')
            fnamepfx            = outfnameZ[:-1]
            outfnameR           = fnamepfx+'R'
            outfnameT           = fnamepfx+'T'
            tr                  = st.select(channel='BHR')[0]
            tr.write(outfnameR, format='mseed')
            tr                  = st.select(channel='BHT')[0]
            tr.write(outfnameT, format='mseed')
        Ndata   += 1
        outstr  += staid
        outstr  += ' '
    print('event : '+ str(otime)+' '+ event_descrip+', '+Mtype+' = '+str(magnitude)+'\n'+\
            str(Ndata)+' data streams are resp removed!')
    if verbose:
        print('STATION CODE: '+outstr)
    print('-----------------------------------------------------------------------------------------------------------')
    return

    
    
    
                
                
                    
        