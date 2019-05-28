#!/bin/bash
i="0"
while [ $i -lt 4 ]
do
ps -eaf | grep mcap_inc_mm4_orig_V2 | grep 25
if [ $? -eq 1 ]
then
./mcap_inc_mm4_orig_V2 -t1 -m2 -h 172.24.3.190 -p 25 -f /root/Vinay/RMS94_CAPACITY/MMSC2RMS/MMSC/mm4_inc_V2_3K_to_4K.xml -r 8 -a 10 -l 100000000000000
else
echo "eq 0 - mstore running, do nothing"
fi
sleep 5
done

