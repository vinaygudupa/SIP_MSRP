
s1=5500230000
s2=6600230000
s3=6700230000
s4=6800230000
s5=6900000000
s6=6900100000
s7=6900200000
local_ip = 'fcff:1:256:172:24:3:0:49'
rmt_ip = 'fcff:1:256:172:24:3:0:190'
term_parties_count = 6
port = 5024
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";"+ str(s3+i) + ";"+ str(s4+i) + ";" + str(term_parties_count) + ";" + str(s5+i) + ";" + str(s6+i) + ";" + str(s7+i) + ";" + str(local_ip) + ";" + str(rmt_ip)
