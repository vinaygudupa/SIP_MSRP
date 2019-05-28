s1=3011102000
s2=3311102000
s3=3111102000
s4=3211102000

s21=3022206000
s22=3322206000
s23=3122206000
s24=3222206000

port=8022
TERM_COUNT_Barred = 5
TERM_COUNT_unBarred = 3
k=0

print "SEQUENTIAL"
for i in range(0,1000):
        print str(s1+i) + ";" + str(s2+i) + ";" + str(port) + ";" + str(s3+i) + ";" + str(s4+i) + ";" + str(TERM_COUNT_Barred)
        print str(s21+i+k) + ";" + str(s22+i+k) + ";" + str(port) + ";" + str(s23+i+k) + ";" + str(s24+i+k) + ";" + str(TERM_COUNT_unBarred)
        print str(s21+i+k+1) + ";" + str(s22+i+k+1) + ";" + str(port) + ";" + str(s23+i+k+1) + ";" + str(s24+i+k+1) + ";" + str(TERM_COUNT_unBarred)
        print str(s21+i+k+2) + ";" + str(s22+i+k+2) + ";" + str(port) + ";" + str(s21+i+k+2) + ";" + str(s22+i+k+2) + ";" + str(TERM_COUNT_unBarred)
        k=k+2
