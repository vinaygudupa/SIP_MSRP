#!/bin/bash
i="0"
while [ $i -lt 4 ]
do
ps -eaf | grep sipp | grep 5002 
if [ $? -eq 1 ]
then
/root/sipp  -sf ORIG.xml -inf MO_MT_90K.csv -m $1 -r $2 -i [fcff:1:256:172:24:3:0:49] -p 5002 [fcff:1:256:172:24:3:0:190]:5060 -nr -l 10000000000 -t tn -max_socket 330
else
echo "eq 0 - mstore running, do nothing"
fi
sleep 5
done

