#/opt/seagull/RMS_67_scripts/run/MSRP_Recv.ksh &
#sleep 1

#/root/msrp/sipp -sf MT_T_rcs.xml -inf MO_MT_90K.csv -i $local_ip -p 5006 $remote_ip:5060 -nr -l 10000000 
/root/sipp -sf ORIG_IMDN.xml -inf MO_MT_90K.csv -i 172.24.1.76 -p 6238 172.24.0.37:5060 -nr -l 10000000 
