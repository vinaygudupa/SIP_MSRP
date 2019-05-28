#./amit.sh
#/root/msrp/sipp  -sf MO_T_rcs.xml -inf MO_MT_90K.csv -m $1 -r $2 -i $local_ip -p 5002 $remote_ip:5060 -nr -l 10000000 
#/root/msrp/sipp  -sf MO_T_caller_clr.xml -inf MO_MT_90K.csv -m $1 -r $2 -i $local_ip -p 5002 $remote_ip:5060 -nr -l 10000000 -master m -slave_cfg slave_cfg2 
/root/sipp  -sf ORIG_IMDN.xml -i [fcff:1:256:172:24:3:0:230] -p 5041 [fcff:1:256:172:24:3:0:190]:5060 -nr -l 10000000000  -t tn -max_socket 330
