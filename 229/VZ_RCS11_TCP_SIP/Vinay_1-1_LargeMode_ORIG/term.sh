#/opt/seagull/RMS_67_scripts/run/MSRP_Recv.ksh &

#/root/msrp/sipp -sf MT_T_rcs.xml -inf MO_MT_90K.csv -i $local_ip -p 5006 $remote_ip:5060 -nd -nr -l 10000000 
/root/sipp -sf TERM.xml -inf MO_MT_90K.csv -i [fcff:1:256:172:24:3:0:228] -p 5052 [fcff:1:256:172:24:3:0:190]:5060 -nd -nr -l 1000000000 -t tn -3pcc [fcff:1:256:172:24:3:0:228]:4561 -max_socket 110 
