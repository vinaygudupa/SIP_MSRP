#!/bin/bash
i="0"
while [ $i -lt 4 ]
do
ps -eaf | grep RMS_ANTI_SPAM | grep 8060
if [ $? -eq 1 ]
then 
./RMS_ANTI_SPAM -address 172.24.1.72:8060
else
sleep 5
fi
done
