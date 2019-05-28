#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=5500110000
port_imdn = 5019
s2=6600110000
port_term = 5020
print "SEQUENTIAL"
for i in range(0,20):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port_term) + ";" + str(port_imdn)

