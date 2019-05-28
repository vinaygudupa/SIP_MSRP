#!/bin/bash
i="0"
while [ $i -lt 4 ]
do
ps -eaf | grep sipp | grep 2003 
if [ $? -eq 1 ]
then
/root/sipp -sf DEREG_NEW.xml -inf DEREG.csv -m $1 -i  [fcff:1:256:172:24:1:0:75] -p 2003 [fcff:1:256:172:24:3:0:190]:5060 -r $2 -t tn -max_socket 330
else
echo "eq 0 - mstore running, do nothing"
fi
sleep 5
done

