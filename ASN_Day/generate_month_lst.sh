#!/bin/bash
#year=(2006 2007 2008 2009 2010 2011 2012)
year=(2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015)
#year=(2004 2005)
#year=(2009 2010 2011)
month=(1 2 3 4 5 6 7 8 9 10 11 12)
monlst=month_US_Continent.lst
if [ -e $monlst ]; then
	rm $monlst
fi	
for y in ${year[@]}; do
	for m in ${month[@]}; do
		echo $y $m >> $monlst
	done
done
exit 
