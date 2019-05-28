s1=2210000000
s2=4410000000
s3=4510000000
s4=4610000000
s5=4710000000
s6=4810000000
s7=4910000000

port=8022
TERM_COUNT = 0

local_ip = 'fcff:1:256:172:24:3:0:231'
remote_ip = 'fcff:1:256:172:24:3:0:190'

print "SEQUENTIAL"
for i in range(0,10000):
        print str(s1+i) + ";" + str(s2+i) + ";" + str(port) + ";" + str(s3+i) + ";" + str(s4+i) + ";" + str(TERM_COUNT) + ";" + str(s5+i) + ";" + str(s6+i) + ";" + str(s7+i) + ";" + str(local_ip) + ";" + str(remote_ip)
