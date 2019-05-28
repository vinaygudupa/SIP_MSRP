#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=3322241000
s2=3022241000

port=7110

print "SEQUENTIAL"
for i in range(0,4000):
	print str(s1+i) + ";" + str(s2+i) + ";" +str(port)


