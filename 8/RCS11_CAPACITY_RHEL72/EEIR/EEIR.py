import asyncio, base64
from re import findall
from random import randint

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()

LOCAL_HOST = file_lines[0].split('=')[1].strip()
LOCAL_PORT = int(file_lines[1].split('=')[1].strip())
REMOTE_HOST = file_lines[2].split('=')[1].strip()
REMOTE_PORT = int(file_lines[3].split('=')[1].strip())
LEGACY_NUM_STARTS_WITH = file_lines[4].split('=')[1].strip()
FAX = file_lines[5].split('=')[1].strip()
FAX_Barred_1 = file_lines[6].split('=')[1].strip()
FAX_Barred_2 = file_lines[7].split('=')[1].strip()
VM = file_lines[8].split('=')[1].strip()
VM_Barred_1 = file_lines[9].split('=')[1].strip()
VM_Barred_2 = file_lines[10].split('=')[1].strip()


FAX_num_range_start = int(FAX.split('-')[0].strip())
FAX_num_range_stop = int(FAX.split('-')[1].strip())
FAX_Barred_1_num_range_start = int(FAX_Barred_1.split('-')[0].strip())
FAX_Barred_1_num_range_stop = int(FAX_Barred_1.split('-')[1].strip())
FAX_Barred_2_num_range_start = int(FAX_Barred_2.split('-')[0].strip())
FAX_Barred_2_num_range_stop = int(FAX_Barred_2.split('-')[1].strip())
VM_num_range_start = int(VM.split('-')[0].strip())
VM_num_range_stop = int(VM.split('-')[1].strip())
VM_Barred_1_num_range_start = int(VM_Barred_1.split('-')[0].strip())
VM_Barred_1_num_range_stop = int(VM_Barred_1.split('-')[1].strip())
VM_Barred_2_num_range_start = int(VM_Barred_2.split('-')[0].strip())
VM_Barred_2_num_range_stop = int(VM_Barred_2.split('-')[1].strip())



async def handle_HTTP(reader, writer):
    global success, failed
    try:
        data_read = await reader.readuntil(b'</soapenv:Envelope>')
        transactionId = findall(b'<transactionId>(.*?)</transactionId>', data_read)
        subscriberId = findall(b'<subscriptionIdData>(.*?)</subscriptionIdData>',data_read)
        subscriberId = str(subscriberId[0].decode())
        if subscriberId.startswith(LEGACY_NUM_STARTS_WITH):
            deviceCapability = 'deviceUPVersion=non-RCS'
        elif VM_num_range_start <= int(subscriberId) <= VM_num_range_stop:
            deviceCapability = 'deviceUPVersion=non-RCS'
        elif VM_Barred_1_num_range_start <= int(subscriberId) <= VM_Barred_1_num_range_stop:
            deviceCapability = 'deviceUPVersion=non-RCS'
        elif VM_Barred_2_num_range_start <= int(subscriberId) <= VM_Barred_2_num_range_stop:
            deviceCapability = 'deviceUPVersion=non-RCS'
        elif FAX_Barred_1_num_range_start <= int(subscriberId) <= FAX_Barred_1_num_range_stop:
            deviceCapability = 'deviceUPVersion=non-RCS'
        elif FAX_Barred_2_num_range_start <= int(subscriberId) <= FAX_Barred_2_num_range_stop:
            deviceCapability = 'deviceUPVersion=non-RCS' 
        elif FAX_num_range_start <= int(subscriberId) <= FAX_num_range_stop:
            deviceCapability = 'deviceUPVersion=non-RCS'
        elif subscriberId :
            deviceCapability = 'deviceUPVersion=rcsup=1'
        else :
            print("subscriber id not found")
        response_part_1 = 'HTTP/1.1 200 OK\r\n' \
                          'Content-Length: ' 
        response_part_2 = '\r\nContent-Type: text/html; encoding=utf8\r\n' \
                          'Connection: close\r\n' \
                          '\r\n'
        response_part_3 = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
                           '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://www.apertio.com/webservice/TmoUsEirSoap/v1"><soapenv:Header/>' \
                           '<soapenv:Body>' \
                           '<v1:SubscriberDeviceQueryRes>' \
                           '<transactionId>' + str(transactionId[0].decode()) + '</transactionId>' \
                           '<userEquipmentInfoType>imeisv</userEquipmentInfoType>' \
                           '<userEquipmentInfoData>35777903132974</userEquipmentInfoData>' \
                           '<ageOfUserEquipmentInfo>42707</ageOfUserEquipmentInfo>' \
                           '<deviceCapability>deviceManufacturer=TCT Mobile Suzhou Limited</deviceCapability>' \
                           '<deviceCapability>deviceModel=OT-363A</deviceCapability>' \
                           '<deviceCapability>deviceBands=GSM 1900,GSM850 (GSM800)</deviceCapability>' \
                           '<deviceCapability>' + deviceCapability + '</deviceCapability>' \
                           '<resultCode>0</resultCode>' \
                           '</v1:SubscriberDeviceQueryRes>' \
                           '</soapenv:Body>' \
                           '</soapenv:Envelope>'
        response = response_part_1 + str(len(response_part_3)) + response_part_2 + response_part_3

        response = response.encode()
        writer.write(response)
        await writer.drain()
        writer.close()
        success += 1
    except Exception as e:
        failed += 1
        print("Exception occured")
    finally:
        print("Success: " + str(success) + "   Failed: " + str(failed))
        return

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_HTTP, LOCAL_HOST, LOCAL_PORT, loop=loop)
server = loop.run_until_complete(coro)

success = 0
failed = 0

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

