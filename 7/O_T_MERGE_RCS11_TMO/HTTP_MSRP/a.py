s1=5500330000
s2=6600330000
term_parties_count = 0
port = 5015
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";" + str(term_parties_count)
