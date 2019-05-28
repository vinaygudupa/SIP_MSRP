s1=5500250000
s2=6600250000
s3=6700250000
s4=6800250000
port = 5024
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";"+ str(s3+i) + ";"+ str(s4+i)
