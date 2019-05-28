#!/bin/bash
/root/sipp -sf REG_ORIG.xml -inf REG_CSV.csv -m $1 -r $2 -i 172.24.1.75 -p 7022 172.24.0.37:5060
