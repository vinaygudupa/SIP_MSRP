s1=5500120000
s2=6600120000
port = 5032
local_ip = 'fcff:1:256:172:24:1:0:73'
rmt_ip = 'fcff:1:256:172:24:3:0:190'
print "SEQUENTIAL"
for i in range(0,10000):
    print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";" + str(local_ip) + ";" + str(rmt_ip)
