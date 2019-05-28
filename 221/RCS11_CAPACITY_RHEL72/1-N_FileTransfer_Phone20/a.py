#Calls

s1=3011104000
s2=3311104000
s3=3111104000
s4=3211104000

s21=3022212000
s22=3322212000
s23=3122212000
s24=3222212000

port=8022

k=0

print "SEQUENTIAL"
for i in range(0,1000):
        print str(s1+i) + ";" +  str(s2+i) + ";"  + str(port) + ";"  + str(s3+i) + ";"  + str(s4+i)
        print str(s21+i+k) + ";"  + str(s22+i+k) + ";"  + str(port) + ";"  + str(s23+i+k) + ";"  + str(s24+i+k)
        print str(s21+i+k+1) + ";"  + str(s22+i+k+1) + ";"  + str(port) + ";"  + str(s23+i+k+1) + ";"  + str(s24+i+k+1)
	print str(s21+i+k+2) + ";"  + str(s22+i+k+2) + ";"  + str(port) + ";"  + str(s23+i+k+2) + ";"  + str(s24+i+k+2)
        k=k+2


