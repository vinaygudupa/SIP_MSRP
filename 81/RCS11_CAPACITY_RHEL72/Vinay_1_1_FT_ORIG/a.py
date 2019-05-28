s1=5500240000
s2=6600240000
port = 5012
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port)
