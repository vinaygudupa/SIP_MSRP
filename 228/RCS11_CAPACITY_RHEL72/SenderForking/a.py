s1=3322221000
s2=3022221000
term_party_count = 3

port=6500

print "SEQUENTIAL"
for i in range(0,8000):
        print str(s1+i) + ";" + str(s2+i) + ";" +str(port) + ";" + str(term_party_count)
