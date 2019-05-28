s1=5800000000
s2=5900000000
term_parties_count = 0
port = 6020
print "SEQUENTIAL"
for i in range(0,100000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";" + str(term_parties_count)
