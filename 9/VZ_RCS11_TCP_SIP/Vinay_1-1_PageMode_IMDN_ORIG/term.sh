#/opt/seagull/RMS_67_scripts/run/MSRP_Recv.ksh &
#sleep 1

#/root/msrp/sipp -sf MT_T_rcs.xml -inf MO_MT_90K.csv -i $local_ip -p 5006 $remote_ip:5060 -nr -l 10000000 
/root/sipp -sf TERM.xml -i [fcff:1:256:172:24:1:0:76] -p 7819 [fcff:1:256:172:24:3:0:190]:5060 -nr -l 10000000000  -t tn -max_socket 110 
