
# networks    = 
with open('_US-TA-StationList.txt', 'rb') as fio:
    for line in fio.readlines():
        print line.split()[1], line.split()[2]
