#!/bin/bash
#/root/RCSe_7_5_Capacity/sipp -sf SUB_NOT.xml -inf MO_1_4_ADHOC.csv -i $local_ip -p 5005 $remote_ip:5060 
/root/sipp -sf SUB_ORIG.xml -inf RE_DEREG.csv -i 172.24.3.231 -p 2000 172.24.0.37:5060
