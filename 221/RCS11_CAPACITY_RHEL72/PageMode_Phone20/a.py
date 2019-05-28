#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=3011105000
s2=3311105000

s21=3022215000
s22=3322215000
port=8110
k=0

print "SEQUENTIAL"
for i in range(0,1000):
	print str(s1+i) + ";" + str(s2+i) + ";" + str(port) 
	print str(s21+i+k) + ";" + str(s22+i+k) + ";" + str(port)
        print str(s21+i+k+1) + ";" + str(s22+i+k+1) + ";" + str(port)
        print str(s21+i+k+2) + ";" + str(s22+i+k+2) + ";" + str(port)
	k=k+2


