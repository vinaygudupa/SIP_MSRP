#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=5500280000
s2=6600280000
port1=7718
port2=7719
print "SEQUENTIAL"

for i in range(0,10000):
  print str(s1+i) + ";" + str(port1) + ";" + str(s2+i)+ ";" + str(port2)
