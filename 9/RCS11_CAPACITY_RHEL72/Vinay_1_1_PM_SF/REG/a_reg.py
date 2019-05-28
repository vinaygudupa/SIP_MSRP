#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Num1 = 2200110000
port1 = 5119
Num2 = 4400110000
port2 = 5120
print "SEQUENTIAL"

for i in range(0,10000):
  print str(Num1+i) + ";" + str(port1) + ";" + str(Num2+i) + ";" + str(port2)
