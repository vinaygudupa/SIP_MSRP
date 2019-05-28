s1=9999210000
s2=9988010000
term_parties_count = 0
port = 5020
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";" + str(term_parties_count)
