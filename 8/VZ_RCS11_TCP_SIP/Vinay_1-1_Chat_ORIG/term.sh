#/opt/seagull/RMS_67_scripts/run/MSRP_Recv.ksh &
#sleep 1

#/root/msrp/sipp -sf MT_T_rcs.xml -inf MO_MT_90K.csv -i $local_ip -p 5006 $remote_ip:5060 -nr -l 10000000 
rm -rf *_counts.csv *.log
/root/sipp -sf TERM.xml -inf MO_MT_90K.csv -i [fcff:1:256:172:24:1:0:75] -p 6020 [fcff:1:256:172:24:3:0:190]:5060 -aa -default_behaviors all -l 10000000 -t tn -3pcc [fcff:1:256:172:24:1:0:75]:4461 -max_socket 110
