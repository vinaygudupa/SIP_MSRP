#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=5500290000
s2=6600290000
port1=7818
port2=7819
print "SEQUENTIAL"

for i in range(0,10000):
  print str(s1+i) + ";" + str(port1) + ";" + str(s2+i)+ ";" + str(port2)
