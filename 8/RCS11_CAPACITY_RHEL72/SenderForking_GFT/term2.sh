#./amit.sh
#/root/msrp/sipp  -sf MO_T_rcs.xml -inf MO_MT_90K.csv -m $1 -r $2 -i $local_ip -p 5002 $remote_ip:5060 -nr -l 10000000
#/root/msrp/sipp  -sf MO_T_caller_clr.xml -inf MO_MT_90K.csv -m $1 -r $2 -i $local_ip -p 5002 $remote_ip:5060 -nr -l 10000000 -master m -slave_cfg slave_cfg2
/root/sipp  -sf TERM2_1.xml -i 172.24.1.75 -p 8024 172.24.0.37:5060 -nr -l 100000000000 -aa 
