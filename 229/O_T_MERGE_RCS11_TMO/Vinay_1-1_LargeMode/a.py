s1=5500120000
s2=6600120000
port = 5032
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port)
