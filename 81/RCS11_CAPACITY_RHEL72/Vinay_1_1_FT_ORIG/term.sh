#/opt/seagull/RMS_67_scripts/run/MSRP_Recv.ksh &
#sleep 1

#/root/msrp/sipp -sf MT_T_rcs.xml -inf MO_MT_90K.csv -i $local_ip -p 5006 $remote_ip:5060 -nr -l 10000000 
/root/Vinay/RMS94_CAPACITY/Vinay_1_1_FT/sipp -sf TERM.xml -i 172.24.3.49 -p 5012 172.24.0.37:5060 -nr -l 10000000000000