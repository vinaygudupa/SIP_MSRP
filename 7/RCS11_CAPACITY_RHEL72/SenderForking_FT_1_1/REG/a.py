#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Orig_Number=3322233000
port_imei_device=9014
port_uuid_device_1=9002
port_uuid_device_2=9004
port_term_party = 9000
print "SEQUENTIAL"
for i in range(0,4000):
  print str(Orig_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1) + ";" + str(port_uuid_device_2) + ";" + str(port_term_party)

