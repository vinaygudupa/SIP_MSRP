#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

s1=5500300000
s2=6600300000
s3=6700300000
s4=6800300000
s5=6900300000
s6=7000300000
s7=7100300000
s8=7200300000
s9=7300300000
s10=7400300000
s11=7500300000
s12=7600300000
orig_imdn_port=5041

print "SEQUENTIAL"

for i in range(0,10000):
  print str(s1+i) + ";"+ str(s2+i) + ";" + str(s3+i) + ";" + str(s4+i) + ";" + str(s5+i) + ";" + str(s6+i) + ";" + str(s7+i) + ";" + str(s8+i) + ";" + str(s9+i) + ";" + str(s10+i) + ";" + str(s11+i) + ";" + str(s12+i) + ";" + str(orig_imdn_port)


