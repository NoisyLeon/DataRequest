
import pyasdf
from obspy.clients.fdsn.client import Client
import obspy.clients.iris
import glob
from functools import partial
from shutil import copyfile
import obspy
import os
import multiprocessing

mondict = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}

class obspyDMTASDF(pyasdf.ASDFDataSet):
    """ An object to for downloaded data manipulation based on ASDF database
    """
    def get_station_data(self, datadir):
        commandfname    = datadir+'/EVENTS-INFO/catalog_info.txt'
        with open(commandfname, 'rb') as f:
            f.readline(); f.readline();
            cline = f.readline()
            cline = cline.split()
        net = ''
        sta = ''
        loc = ''
        cha = ''
        for i in xrange(len(cline)):
            if cline[i] == '--net':
                net = cline[i+1]
            if cline[i] == '--sta':
                sta = cline[i+1]
            if cline[i] == '--loc':
                loc = cline[i+1]
            if cline[i] == '--cha':
                cha = cline[i+1]
        self.get_stations(network=net, station=sta, location=loc, channel=cha)
        return
    
    def get_StaInv(self, source='IRIS-DMC'):
        """
        Get station inventory object
        """
        self.inv    =   obspy.core.inventory.inventory.Inventory(networks=[], source=source)
        for staid in self.waveforms.list():
            self.inv    += self.waveforms[staid].StationXML
        return
    
    
    def prepare_continuous_data(self, datadir, outdir, chalst=['LHZ', 'LHE', 'LHN'], remove_response=False, verbose=True):
        """
        Prepare continuous data for ambient noise cross-correlation computation
        =======================================================================================================
        Input Parameters:
        datadir         - data directory
        outdir          - output directory
        chalst          - channel list
        inasdf          - read data in ASDF or not (NOT implemented yet)
        remove_response - get the response-removed data or not
        =======================================================================================================
        """
        pattern = datadir+'/continuous*'
        try:
            inv = self.inv
        except:
            self.get_StaInv()
            inv = self.inv
        dirLst = glob.glob(pattern)
        for directory in dirLst:
            _prepare_continuous_data(datadir=directory, outdir=outdir, inv=inv, chalst=chalst, remove_response=remove_response, verbose=verbose)
    
    def prepare_continuous_data_mp(self, datadir, outdir, subsize=1000, chalst=['LHZ', 'LHE', 'LHN'],
                inasdf=False, remove_response=False, nprocess=2, verbose=False):
        """
        Parallel version of prepare_continuous_data
        =======================================================================================================
        Input Parameters:
        datadir         - data directory
        outdir          - output directory
        subsize         - sub size for parallel computation
        chalst          - channel list
        inasdf          - read data in ASDF or not (NOT implemented yet)
        remove_response - get the response-removed data or not
        nprocess        - number of process
        =======================================================================================================
        """
        pattern = datadir+'/continuous*'
        try:
            inv = self.inv
        except:
            self.get_StaInv()
            inv = self.inv
        dirLst = glob.glob(pattern)
        if len(dirLst) > subsize:
            Nsub = int(len(dirLst)/subsize)
            for isub in xrange(Nsub):
                print 'Subset:', isub,'in',Nsub,'sets'
                cdir        = dirLst[isub*subsize:(isub+1)*subsize]
                prepare_data= partial(_prepare_continuous_data, outdir=outdir, inv=inv, chalst=chalst, remove_response=remove_response, verbose=verbose)
                pool        = multiprocessing.Pool(processes=nprocess)
                pool.map(prepare_data, cdir) #make our results with a map call
                pool.close() #we are not adding any more processes
                pool.join() #tell it to wait until all threads are done before going on
            cdir        = dirLst[(isub+1)*subsize:]
            prepare_data= partial(_prepare_continuous_data, outdir=outdir, inv=inv, chalst=chalst, remove_response=remove_response, verbose=verbose)
            pool        = multiprocessing.Pool(processes=nprocess)
            pool.map(prepare_data, cdir) #make our results with a map call
            pool.close() #we are not adding any more processes
            pool.join() #tell it to wait until all threads are done before going on
        else:
            prepare_data= partial(_prepare_continuous_data, outdir=outdir, inv=inv, chalst=chalst, remove_response=remove_response, verbose=verbose)
            pool        = multiprocessing.Pool(processes=nprocess)
            pool.map(prepare_data, dirLst) #make our results with a map call
            pool.close() #we are not adding any more processes
            pool.join() #tell it to wait until all threads are done before going on
        print 'End of multiprocessing getting continuous data !'

    
    def get_stations(self, startdate=None, enddate=None,  network=None, station=None, location=None, channel=None,
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
        try: starttime      = obspy.core.utcdatetime.UTCDateTime(startdate)
        except: starttime   = None
        try: endtime        = obspy.core.utcdatetime.UTCDateTime(enddate)
        except: endtime     = None
        client  = Client('IRIS')
        inv     = client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, channel=channel, 
                    minlatitude=minlatitude, maxlatitude=maxlatitude, minlongitude=minlongitude, maxlongitude=maxlongitude,
                        latitude=latitude, longitude=longitude, minradius=minradius, maxradius=maxradius, level='channel')
        self.add_stationxml(inv)
        try: self.inv       += inv
        except: self.inv    = inv
        return 

def _prepare_continuous_data(datadir, outdir, inv, chalst=['LHZ', 'LHE', 'LHN'], remove_response=False, verbose=True):
    wavepfx = datadir+'/'
    for network in inv.networks:
        net_code    = network.code
        for station in network.stations:
            sta_code    = station.code
            stla    = station.latitude; stlo    = station.longitude
            for cha in chalst:
                # # # if not remove_response:
                # # #     wfpattern   = datadir+'/raw/'+net_code+'.'+sta_code+'.*'+cha
                # # #     wfLst       = glob.glob(wfpattern)
                # # #     if len(wfLst) == 0: continue
                # # #     else:
                # # #         wfname  = wfLst[0]
                # # # else:
                # # #     wfpattern   = datadir+'/processed/'+net_code+'.'+sta_code+'.*'+cha
                # # #     wfLst       = glob.glob(wfpattern)
                # # #     if len(wfLst) == 0: continue
                # # #     else:
                # # #         wfname  = wfLst[0]
                wfpattern   = datadir+'/raw/'+net_code+'.'+sta_code+'.*'+cha
                wfLst       = glob.glob(wfpattern)
                if len(wfLst) == 0: continue
                else:
                    wfname  = wfLst[0]        
                tr          = obspy.read(wfname)[0]
                if tr.stats.npts*tr.stats.delta < 3600.*10.:
                    print 'Too many holes, skipping data: '+ wfname
                    continue
                temp_time   = tr.stats.starttime+1000.
                stime       = obspy.UTCDateTime(temp_time.date)+1.
                etime       = stime+3600.*24.-1.
                npts        = (3600.*24.-1.)/tr.stats.delta
                if verbose: print wfname
                tr.interpolate(1./tr.stats.delta, starttime=stime, npts=npts)
                # # # tr.trim(starttime=stime, endtime=etime)
                tr.stats.sac={}
                tr.stats.sac['stlo'] = stlo; tr.stats.sac['stla'] = stla
                year    = stime.year; month = mondict[stime.month]; day = stime.day
                doutdir = outdir+'/'+str(year)+'.'+month+'/'+str(year)+'.'+month+'.'+str(day)
                if not os.path.isdir(doutdir):
                    os.makedirs(doutdir)
                tempstr         = wfname.split('/')[-1]
                loc_code        = tempstr.split('.')[-2]
                if not remove_response:
                    outsacfname     = doutdir+'/'+str(year)+'.'+month+'.'+str(day)+'.'+sta_code+'.'+cha+'.SAC'
                    outrespfname    = doutdir+'/RESP.'+tempstr
                    client          = obspy.clients.iris.Client()
                    try:
                        client.resp(network=net_code, station=sta_code, channel=cha, location=loc_code, starttime=stime, endtime=etime, filename=outrespfname)
                        tr.write(outsacfname, format='SAC')
                    except:
                        continue
                else:
                    respfname       = datadir+'/resp/STXML.'+tempstr
                    if not os.path.isfile(respfname):
                        print 'WARNNING: No resp file for : '+str(year)+'.'+month+'.'+str(day)+'.'+cha+'.SAC'
                        continue
                    inv         = obspy.read_inventory(respfname)
                    tr.attach_response(inv)
                    tr.detrend()
                    tr.remove_response(pre_filt=(0.001, 0.005, 1, 100.0))
                    outsacfname = doutdir+'/ft_'+str(year)+'.'+month+'.'+str(day)+'.'+sta_code+'.'+cha+'.SAC'
                    tr.write(outsacfname, format='SAC')
                    with open(outsacfname+'_rec', 'wb') as f:
                        f.writelines('0\t84001\n') 
            
                    
                    
                
                
    
    
    