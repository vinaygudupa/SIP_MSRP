#!/bin/bash
#/root/RCSe_7_5_Capacity/sipp -sf reg_caller.xml -inf MO_1_4_ADHOC.csv -m $1 -r $2 -i $local_ip -p 5004 $remote_ip:5060 -l 1000000 -watchdog_minor_threshold 10000  -watchdog_minor_maxtriggers 1200 -watchdog_major_threshold 20000 -watchdog_major_maxtriggers 2000 -watchdog_reset 1000 -t tn -max_socket 240000 
/root/sipp -sf REG_ORIG.xml -inf REG_CSV.csv -m $1 -r $2 -i 172.24.3.227 -p 7014 172.24.0.37:5060
