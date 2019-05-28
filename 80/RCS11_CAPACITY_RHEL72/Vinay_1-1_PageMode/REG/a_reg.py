#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Num1 = 5500110000
port1 = 5019
Num2 = 6600110000
port2 = 5020
print "SEQUENTIAL"

for i in range(0,10000):
  print str(Num1+i) + ";" + str(port1) + ";" + str(Num2+i) + ";" + str(port2)
