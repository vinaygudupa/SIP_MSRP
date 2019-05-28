s1=3322234000
s2=3311104000
s3=3311120000
s4=3311121000

s21=3322235000
s22=3322238000
s23=3322241000
s24=3322244000

port=5024  
k=0

print "SEQUENTIAL"
for i in range(0,1000):
	print str(s1+i) + ";" + str(s2+i) + ";" +str(port) + ";" + str(s3+i) + ";" + str(s4+i)
	print str(s21+i+k) + ";" + str(s22+i+k) + ";" +str(port) + ";" + str(s23+i+k) + ";" + str(s24+i+k)
	print str(s21+i+k+1) + ";" + str(s22+i+k+1) + ";" +str(port) + ";" + str(s23+i+k+1) + ";" + str(s24+i+k+1)
	print str(s21+i+k+2) + ";" + str(s22+i+k+2) + ";" +str(port) + ";" + str(s23+i+k+2) + ";" + str(s24+i+k+2)
	k = k + 2
