
s1=5500230000
s2=6600230000
s3=6700230000
s4=6800230000
term_parties_count = 3
port = 5024
print "SEQUENTIAL"
for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(port) + ";"+ str(s3+i) + ";"+ str(s4+i) + ";" + str(term_parties_count)
