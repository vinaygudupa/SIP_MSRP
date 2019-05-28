s1=3011103000
s2=3311103000

s21=3022209000
s22=3322209000

port=8078
k=0

print "SEQUENTIAL"
for i in range(0,1000):
        print str(s1+i) + ";" + str(s2+i) + ";" + str(port)
        print str(s21+i+k) + ";" + str(s22+i) + ";" + str(port)
        print str(s21+i+k+1) + ";" + str(s22+i+k+1) + ";" + str(port)
	print str(s21+i+k+2) + ";" + str(s22+i+k+2) + ";" + str(port)
        k=k+2
