from aiohttp import web
from re import findall
from asyncio import sleep

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

success = 0
failed = 0
display_task_started = False

async def display_count():
    while True:
        print("Success : " + str(success) + " Failed : " + str(failed))
        await sleep(5)


async def handle_post(request):
    global success, failed, display_task_started
    if not display_task_started:
        print("Display started")
        app.loop.create_task(display_count())
        display_task_started = True
    try:
        deviceCapability = ''
        data_read = await request.read()
        transactionId = findall(b'<transactionId>(.*?)</transactionId>', data_read)
        subscriberId = findall(b'<subscriptionIdData>(.*?)</subscriptionIdData>', data_read)
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
        elif subscriberId:
            deviceCapability = 'deviceUPVersion=rcsup=1'
        else:
            print("subscriber id not found")

        response_final = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
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
        success += 1
        return web.Response(status=200, body=response_final, content_type='text/html')
    except Exception as e:
        failed += 1
        return web.Response(status=404)

app = web.Application()
app.add_routes([web.post('/', handle_post)])
web.run_app(app, host=LOCAL_HOST, port=LOCAL_PORT)
