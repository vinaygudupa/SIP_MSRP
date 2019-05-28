s1=2200100000
s2=4400100000
port = 5005
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port)
