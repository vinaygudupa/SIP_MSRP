s1=3322237000
s2=3022237000
s3=3122237000
s4=3222237000

port=5024

print "SEQUENTIAL"
for i in range(0,4000):
        print str(s1+i) + ";" + str(s2+i) + ";" +str(port) + ";" + str(s3+i) + ";" + str(s4+i)
