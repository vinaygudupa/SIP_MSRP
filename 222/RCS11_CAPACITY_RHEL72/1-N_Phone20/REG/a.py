Term_Number=3311102000
port_imei_device=8022
port_uuid_device_1=8024
port_uuid_device_2=8026

print "SEQUENTIAL"
for i in range(0,1000):
  print str(Term_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1)+ ";" + str(port_uuid_device_2)

Term_Number=3322206000

for i in range(0,3000):
  print str(Term_Number+i) + ";" + str(port_imei_device) + ";" + str(port_uuid_device_1)+ ";" + str(port_uuid_device_2)
