#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Num = 5500130000
port = 6018

print "SEQUENTIAL"
for i in range(0,100000):
	print str(Num+i) + ";" + str(port)
