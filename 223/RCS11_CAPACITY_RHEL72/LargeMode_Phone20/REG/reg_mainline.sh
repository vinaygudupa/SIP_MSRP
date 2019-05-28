#!/bin/bash
/root/sipp -sf REG_MAINLINE.xml -inf REG_CSV.csv -m $1 -r $2 -i 172.24.3.231 -p 7000 172.24.0.37:5060
