#/opt/seagull/RMS_67_scripts/run/MSRP_Recv.ksh &

#/root/msrp/sipp -sf MT_T_rcs.xml -inf MO_MT_90K.csv -i $local_ip -p 5006 $remote_ip:5060 -nd -nr -l 10000000 
/root/sipp -sf TERM.xml -i 172.24.3.228 -p 5052 172.24.0.37:5060 -nd -nr -l 1000000000 
