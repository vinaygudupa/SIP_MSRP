#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Num = 9399400000
port = 5044
print "SEQUENTIAL"

for i in range(0,100000):
  print str(Num+i) + ";" + str(port)
