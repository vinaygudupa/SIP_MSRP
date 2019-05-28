s1=3322214000
s2=3311102000
s3=3311118000
s4=3311119000

s21=3322215000
s22=3322218000
s23=3322221000
s24=3322224000

port=8024
TERM_COUNT_Barred = 5
TERM_COUNT_unBarred = 3
k=0
SENDER_DEVICE_Barred = 17
SENDER_DEVICE_UnBarred = 11

print "SEQUENTIAL"
for i in range(0,1000):
    print str(s1+i) + ";" + str(s2+i) + ";" + str(port) + ";" + str(TERM_COUNT_Barred) + ";" + str(s3+i) + ";" + str(s4+i) + ";" + str(SENDER_DEVICE_Barred)
    print str(s21+i+k) + ";" + str(s22+i+k) + ";" + str(port) + ";" + str(TERM_COUNT_unBarred) + ";" + str(s23+i+k) + ";" + str(s24+i+k) + ";" + str(SENDER_DEVICE_UnBarred)
    print str(s21+i+k+1) + ";" + str(s22+i+k+1) + ";" + str(port) + ";" + str(TERM_COUNT_unBarred) + ";" + str(s23+i+k+1) + ";" + str(s24+i+k+1) + ";" + str(SENDER_DEVICE_UnBarred)
    print str(s21+i+k+2) + ";" + str(s22+i+k+2) + ";" + str(port) + ";" + str(TERM_COUNT_unBarred) + ";" + str(s23+i+k+2) + ";" + str(s24+i+k+2) + ";" + str(SENDER_DEVICE_UnBarred)
    k=k+2
