
s1=5500250000
s2=6600250000
s3=6700250000
s4=6800250000
s5=6900800000
s6=6900900000
s7=6901000000
term_parties_count = 6
port = 6024
local_ip = 'fcff:1:256:172:24:3:0:49'
rmt_ip = 'fcff:1:256:172:24:3:0:190'
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";"+ str(s3+i) + ";"+ str(s4+i) + ";" + str(term_parties_count) + ";" + str(s5+i) + ";" + str(s6+i) + ";" + str(s7+i) + ";" + str(local_ip) + ";" + str(rmt_ip)
