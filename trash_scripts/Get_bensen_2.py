import obspy
import glob
# import 

mondict = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}
datadir = '/work3/leon/breq_fast/freq_no_time_no'
datadir = '/work3/leon/breq_fast/freq_no_time_one'
datadir = '/work3/leon/breq_fast/freq_no_time_run'

datadir = '/work3/leon/breq_fast/freq_yes_time_no'
datadir = '/work3/leon/breq_fast/freq_yes_time_one'
datadir = '/work3/leon/breq_fast/freq_yes_time_run'


start_date  = '2004-01-01'

end_date    = '2005-01-01'

sta1        = 'ANMO'; sta2='HRV'

stime=obspy.UTCDateTime(start_date); etime = obspy.UTCDateTime(end_date)

dyear  = etime.year - stime.year
dmonth = etime.month - stime.month

cyear = stime.year
cmonth= stime.month

outtr=obspy.Trace()
d = 0
while( not (cyear == etime.year and cmonth == etime.month) ):
    dmonth = mondict[cmonth]
    sacfname = datadir + '/'+str(cyear)+'.'+dmonth+'/COR/'+sta1+'/COR_'+sta1+'_'+sta2+'.SAC'
    inTr = obspy.read(sacfname)[0]
    if outtr.stats.npts==0:
        outtr   = inTr.copy()
        d       = outtr.stats.sac.user0
    else:
        d       += inTr.stats.sac.user0
        outtr.data+=inTr.data
    
    if cmonth != 12: cmonth+=1
    else:
        cmonth=1; cyear+=1

outtr.stats.sac.user0 = d
outtr.write(datadir+'/COR_'+sta1+'_'+sta2+'.SAC', format='SAC')