s1=5500270000
s2=6600270000
port = 5052
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port)
