#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=5500300000
s2=6600300000
s3=6700300000
s4=6800300000
s5=6901600000
s6=6901700000
s7=6901800000
orig_imdn_port=7041

print "SEQUENTIAL"

for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(s3+i) + ";" + str(s4+i) + ";" + str(s5+i) + ";" + str(s6+i) + ";" + str(s7+i) + ";" + str(orig_imdn_port)


