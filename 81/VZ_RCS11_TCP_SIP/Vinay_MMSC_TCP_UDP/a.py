#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=9199200000
s2=9199300000
local_ip = 'fcff:1:256:172:24:3:0:49'
remote_ip = 'fcff:1:256:172:24:3:0:190'
print "SEQUENTIAL"

for i in range(0,10000):
  print str(s1+i) + ";" + str(s2+i) + ";" + str(local_ip) + ";" + str(remote_ip)

