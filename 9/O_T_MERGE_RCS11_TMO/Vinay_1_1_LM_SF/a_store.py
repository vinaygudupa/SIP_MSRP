s1=2200260000
s2=4400260000
port = 5032
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port)
