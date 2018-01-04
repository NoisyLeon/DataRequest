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

class DMTASDF(pyasdf.ASDFDataSet):
    
    def copy_catalog(self):
        print('Copying catalog from ASDF to memory')
        self.cat    = self.events.copy()
        
    def remove_resp_catalog(self, datadir, verbose=False, fs=40.):
        evnumb              = 0
        try:
            print self.cat
        except AttributeError:
            self.copy_catalog()
            
        
            
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

    
    
    
                
                
                    
        