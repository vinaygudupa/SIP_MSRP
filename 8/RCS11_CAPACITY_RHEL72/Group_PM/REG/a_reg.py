#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Num1 = 5500300000
port1 = 5040
Num2 = 6600300000
port2 = 5041
print "SEQUENTIAL"

for i in range(0,10000):
  print str(Num1+i) + ";" + str(port1) + ";" + str(Num2+i) + ";" + str(port2)
