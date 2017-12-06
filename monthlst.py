import obspy

start_date  ='19910101'
end_date    ='20101201'

outfname    = 'ASN/Alaska_month_1991_2010.lst'

stime       = obspy.UTCDateTime(start_date)
etime       = obspy.UTCDateTime(end_date)


with open(outfname, 'w') as fid:
    while(stime <= etime):
        fid.writelines(str(stime.year)+' '+str(stime.month)+'\n')
        try:
            stime.month += 1
        except ValueError:
            stime.year  += 1
            stime.month = 1
