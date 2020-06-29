# import obspy
# 
# start_date  ='20190201'
# end_date    ='20190228'
# outfname    = 'ASN/Alaska_month_2019_2.lst'
# stime       = obspy.UTCDateTime(start_date)
# etime       = obspy.UTCDateTime(end_date)
# 
# with open(outfname, 'w') as fid:
#     while(stime <= etime):
#         fid.writelines(str(stime.year)+' '+str(stime.month)+'\n')
#         try:
#             stime.month += 1
#         except ValueError:
#             stime.year  += 1
#             stime.month = 1



import os
import obspy
import glob
datadir     = '/backup/leon/COR_USCON_dir/seed_data'
start_date  ='20130101'
end_date    ='20151231'
stime       = obspy.UTCDateTime(start_date)
etime       = obspy.UTCDateTime(end_date)
monthdict   = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}
month       = stime.month - 1
pfx         = 'LF_'
yearlst     = []
monthlst    = []
while(stime < etime):
    # print stime
    if month < stime.month:
        month   += 1
        print 'Checking data: '+str(stime.year)+'.'+monthdict[stime.month]
    fname_pattern   = datadir+'/'+pfx+str(stime.year)+'.'+monthdict[stime.month]+'.'+str(stime.day)+'*'
    try:
        fname           = glob.glob(fname_pattern)[0]
    except:
        if len(yearlst) == 0:
            yearlst.append(stime.year)
            monthlst.append(stime.month)
        elif yearlst[-1] != stime.year or monthlst[-1] != stime.month:
            yearlst.append(stime.year)
            monthlst.append(stime.month)
        else:
            pass
    if stime.month == 12 and stime.day == 31:
        stime   = obspy.UTCDateTime(str(stime.year + 1)+'0101')
        month   = 0
    else:
        stime.julday += 1

outfname    = 'ASN/USCON_2013_2015.lst'
with open(outfname, 'w') as fid:
    L   = len(monthlst)
    for i in range(L):
        fid.writelines(str(yearlst[i])+' '+str(monthlst[i])+'\n')
