#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Orig_Number=3322229000
port_imei_device=8022
port_uuid_device_1=8028
port_uuid_device_2=8030
port_term_party=8024

print "SEQUENTIAL"
for i in range(0,4000):
  print str(Orig_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1) + ";" + str(port_uuid_device_2) + ";" + str(port_term_party)