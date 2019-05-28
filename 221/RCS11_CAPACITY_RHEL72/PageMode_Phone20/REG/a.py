#for i in range(0,10000):
#  print str(start+i) + ";[authentication username=" + str(start+i) + "@mavenir.lab password=mavenir];mavenir.lab"

Term_Number=3311105000
port_imei_device=8110
port_uuid_device_1=8112
port_uuid_device_2=8114

print "SEQUENTIAL"
for i in range(0,1000):
  print str(Term_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1)+ ";" + str(port_uuid_device_2) 

Term_Number=3322215000

for i in range(0,3000):
  print str(Term_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1)+ ";" + str(port_uuid_device_2)

