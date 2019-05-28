local_ip = 'fcff:1:256:172:24:3:0:32'
rmt_ip = 'fcff:1:256:172:24:3:0:190'
print "SEQUENTIAL"
for i in range(0,10000000):
	print str(local_ip) + ";" + str(rmt_ip)
