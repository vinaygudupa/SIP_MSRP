s1=5500000000
s2=6600000000
term_parties_count = 1
port = 5020
print "SEQUENTIAL"
for i in range(0,100000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";" + str(term_parties_count)
