#!/bin/bash
i="0"
while [ $i -lt 4 ]
do
ps -eaf | grep sipp | grep 2001
if [ $? -eq 1 ]
then
/root/sipp -sf REG.xml -inf REG.csv -m $1 -i [fcff:1:256:172:24:1:0:75] -p 2001 [fcff:1:256:172:24:3:0:190]:5060 -r $2 -t tn -max_socket 110
else
echo "eq 0 - mstore running, do nothing"
fi
sleep 5
done

