#!/bin/bash
#/root/RCSe_7_5_Capacity/sipp -sf SUB_NOT.xml -inf MO_1_4_ADHOC.csv -i $local_ip -p 5005 $remote_ip:5060 
/root/sipp -sf SUB_ORIG.xml -inf REG_CSV.csv -i 172.24.1.74 -p 9014 172.24.0.37:5060
