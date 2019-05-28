#/opt/seagull/RMS_67_scripts/run/MSRP_Recv.ksh &
#sleep 1

#/root/msrp/sipp -sf MT_T_rcs.xml -inf MO_MT_90K.csv -i $local_ip -p 5006 $remote_ip:5060 -nr -l 10000000 
rm -rf *_counts.csv
rm -rf *_errors.log
/root/sipp -sf TERM_ICSCF.xml -inf MO_MT_90K.csv -i [fcff:1:256:172:24:3:0:32] -p 4900 [fcff:1:256:172:24:3:0:190]:5060 -l 1000000000000 -aa -default_behaviors all -master m -slave_cfg slave_config_file -t tn -max_socket 110
