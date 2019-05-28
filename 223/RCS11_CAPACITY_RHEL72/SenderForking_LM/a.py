s1=3322245000
s2=3022245000

port=9000

print "SEQUENTIAL"
for i in range(0,4000):
        print str(s1+i) + ";" + str(s2+i) + ";" +str(port)
