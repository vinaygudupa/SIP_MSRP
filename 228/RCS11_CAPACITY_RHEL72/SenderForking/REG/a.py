#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Orig_Number=3322221000
port_imei_device=6514
port_uuid_device_1=6502
port_uuid_device_2=6504
port_term_party=6500

print "SEQUENTIAL"
for i in range(0,8000):
  print str(Orig_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1) + ";" + str(port_uuid_device_2) + ";" + str(port_term_party)
