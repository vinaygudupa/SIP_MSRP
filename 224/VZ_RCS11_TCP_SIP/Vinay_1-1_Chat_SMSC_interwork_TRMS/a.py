s1=9999210000
s2=9988010000
term_parties_count = 0
port = 5020
local_ip = 'fcff:1:256:172:24:3:0:16'
rmt_ip = 'fcff:1:256:172:24:3:0:190'
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";" + str(term_parties_count) + ";" + str(local_ip) + ";" + str(rmt_ip)
