#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=9299100000
s2=9299300000
print "SEQUENTIAL"
for i in range(0,100000):
	print str(s1+i) + ";" + str(s2+i) + ";rcse-dls-capacity.mavenir.lab;" + "172.24.3.34;5042"
