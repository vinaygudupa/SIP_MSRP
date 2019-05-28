#/opt/seagull/RMS_67_scripts/run/MSRP_Recv.ksh &
#sleep 1

#/root/msrp/sipp -sf MT_T_rcs.xml -inf MO_MT_90K.csv -i $local_ip -p 5006 $remote_ip:5060 -nr -l 10000000 
/root/sipp -sf TERM_1.xml -inf MO_MT_90K_1.csv -i 172.24.3.32 -p 5042 172.24.0.34:5060 -nr -l 1000000000000 
