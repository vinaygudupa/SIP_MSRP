s1=5500340000
s2=6600340000
term_parties_count = 1
port = 5220
local_ip = 'fcff:1:256:172:24:3:0:51'
remote_ip = 'fcff:1:256:172:24:3:0:190'
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";" + str(term_parties_count) + ";" + str(local_ip) + ";" + str(remote_ip)
