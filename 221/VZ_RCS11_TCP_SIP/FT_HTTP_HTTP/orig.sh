#./amit.sh
#/root/msrp/sipp  -sf MO_T_rcs.xml -inf MO_MT_90K.csv -m $1 -r $2 -i $local_ip -p 5018 $remote_ip:5060 -nr -l 10000000 
#/root/msrp/sipp  -sf MO_T_caller_clr.xml -inf MO_MT_90K.csv -m $1 -r $2 -i $local_ip -p 5018 $remote_ip:5060 -nr -l 10000000 -master m -slave_cfg slave_cfg2 
/root/sipp  -sf ORIG.xml -inf MO_MT_90K.csv -m $1 -r $2 -i [fcff:1:256:172:24:3:0:51]  -p 5018 [fcff:1:256:172:24:3:0:190]:5060 -nr -l 10000000000000 -3pcc [fcff:1:256:172:24:3:0:51]:4460 -max_socket 110 -t tn