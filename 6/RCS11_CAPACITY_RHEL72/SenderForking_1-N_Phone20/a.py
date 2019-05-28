s1=3322229000
s2=3022229000
term_party_count = 5
s3=3122229000
s4=3222229000

port=5024

print "SEQUENTIAL"
for i in range(0,4000):
        print str(s1+i) + ";" + str(s2+i) + ";" +str(port) + ";" + str(term_party_count) + ";" + str(s3+i) + ";" + str(s4+i)
