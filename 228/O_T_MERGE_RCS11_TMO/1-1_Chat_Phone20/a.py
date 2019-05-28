s1=3322200000
s2=3311100000

s21=3322202000
s22=3322208000
port=8000
TERM_COUNT_Barred = 7
TERM_COUNT_unBarred = 5
k=0

print "SEQUENTIAL"
for i in range(0,2000):
        print str(s1+i) + ";" + str(s2+i) + ";" + str(port) + ";" + str(TERM_COUNT_Barred)
        print str(s21+i+k) + ";" + str(s22+i+k) + ";" + str(port) + ";" + str(TERM_COUNT_unBarred)
        print str(s21+i+k+1) + ";" + str(s22+i+k+1) + ";" + str(port) + ";" + str(TERM_COUNT_unBarred)
        print str(s21+i+k+2) + ";" + str(s22+i+k+2) + ";" + str(port) + ";" + str(TERM_COUNT_unBarred)
        k=k+2
