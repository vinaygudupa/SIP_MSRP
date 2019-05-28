#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Orig_Number=3322241000
port_imei_device=7108
port_uuid_device_1=7112
port_uuid_device_2=7114
port_term_party = 7110
print "SEQUENTIAL"
for i in range(0,4000):
  print str(Orig_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1) + ";" + str(port_uuid_device_2) + ";" + str(port_term_party)

