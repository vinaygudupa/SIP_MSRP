#!/bin/bash
i="0"
while [ $i -lt 4 ]
do
ps -eaf | grep sipp | grep 2550 
if [ $? -eq 1 ]
then
/root/sipp -sf reREG.xml -inf reREG.csv -m $1 -i  [fcff:1:256:172:24:1:0:75] -p 2550 [fcff:1:256:172:24:3:0:190]:5060 -r $2 -t tn -max_socket 330
else
echo "eq 0 - mstore running, do nothing"
fi
sleep 5
done

