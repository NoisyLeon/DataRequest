import obspy

cat     = obspy.read_inventory('ALASKA_BH.xml')
stime   = obspy.UTCDateTime('25000101')
etime   = obspy.UTCDateTime('19000101')
for network in cat:
    if network.code != 'AK':
        continue
    for sta in network:
        if sta.start_date < stime:
            stime = sta.start_date
        if sta.end_date > etime:
            etime = sta.end_date

print stime
print etime

