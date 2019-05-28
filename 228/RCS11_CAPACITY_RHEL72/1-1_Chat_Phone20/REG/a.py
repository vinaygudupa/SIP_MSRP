Term_Number=3311100000
port_imei_device=8000
port_uuid_device_1=8002
port_uuid_device_2=8004

print "SEQUENTIAL"
for i in range(0,2000):
  print str(Term_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1)+ ";" + str(port_uuid_device_2)

Term_Number=3322200000

for i in range(0,6000):
  print str(Term_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1)+ ";" + str(port_uuid_device_2)
