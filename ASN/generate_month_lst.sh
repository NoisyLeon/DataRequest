#!/bin/bash
year=(1991)
month=(1 2 3 4 5 6 7 8 9 10 11 12)
monlst=month_EARS.lst
if [ -e $monlst ]; then
	rm $monlst
fi	
for y in ${year[@]}; do
	for m in ${month[@]}; do
		echo $y $m >> $monlst
	done
done
exit 
