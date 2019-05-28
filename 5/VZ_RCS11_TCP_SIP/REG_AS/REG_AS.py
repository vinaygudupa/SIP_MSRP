from aiohttp import web
from re import findall
from asyncio import sleep
import time, base64

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()

LOCAL_HOST = file_lines[0].split('->')[1].strip()
LOCAL_PORT = int(file_lines[1].split('->')[1].strip())
REMOTE_HOST = file_lines[2].split('->')[1].strip()
REMOTE_PORT = int(file_lines[3].split('->')[1].strip())
FEATURES = file_lines[4].split('->')[1].strip()

display_task_started = False
GET_404 = 0
GET_200 = 0
POST_201 = 0
UPDATE_200 = 0
DELETE_200 = 0

dict_range_data = {}
reg_dereg_dict = {}

for i in file_lines:
    if i.startswith("range_"):
        data = i.split('--')
        name = data[0].strip().split('->')[1].strip()
        start_num = int(data[1].strip())
        range_num = int(data[2].strip())
        scscf = data[3].split(',')
        for j in range(0,len(scscf)):
            scscf[j] = scscf[j].strip()
        dict_range_data[name] = [start_num,(start_num+range_num-1),scscf]
    else:
        continue

async def display_count():
    while True:
        await sleep(5)
        print("GET_404 : " + str(GET_404) + "   GET_200 : " + str(GET_200) + "   POST_201 : " + str(POST_201)
              + "    UPDATE_200 : " + str(UPDATE_200) + "   DELETE_200 : " + str(DELETE_200))

def convert_to_base64(x):
    return base64.b64encode((x).encode()).decode()

async def handle_get(request):
    global display_task_started, GET_200, GET_404, reg_dereg_dict
    if not display_task_started:
        print("Display started")
        app.loop.create_task(display_count())
        display_task_started = True
    req_url = str(request.url)
    destNum = findall('destUserId=1(\d{10})', req_url)
    if destNum:
        destNum = destNum[0]
        dest_num_int = int(destNum)
        for i in dict_range_data:
            if dest_num_int >= dict_range_data[i][0] and dest_num_int <= dict_range_data[i][1]:
                if i == 'REG':
                    GET_404 += 1
                    return web.Response(status=404)
                else:
                    contact = ''
                    scscf_addr = dict_range_data[i][2][0]
                    impu = "sip:+1" + str(dest_num_int) + "@rcse-dls-capacity.mavenir.lab"
                    tp_data = '{"regInfo":{"msisdn":"1' + destNum + '",\r\n' \
                                + '"scscfName":"' + scscf_addr + '",\r\n' \
                                + '"impu":"' + impu + '",\r\n' \
                                + '"CSeq":"1",\r\n' \
                                + '"expires":"3600",\r\n' \
                                + '"registration": {\r\n"aor":"' + impu + '",\r\n' \
                                + '"contacts":[\r\n'
                    for j in range(len(dict_range_data[i][2])):
                        ip_port = dict_range_data[i][2][j].split(":[")
                        ip_port_1 = ip_port[1].split("]:")
                        ipv6_addr = '[' + ip_port_1[0] + ']'
                        port_num = ip_port_1[1]
                        if j == 0:
                            sip_instance = "urn:gsma:imei:" + destNum[0:8] + "-" + destNum[8:10] + "0000-0"
                            UserAgent = "IM-client/OMA1.0 moto/Moto%20E-7.1.1 DTAG/RCSEAndr-9.99-B9556-debug Orange-RCS/v2.5.18.r553"
                        else:
                            sip_instance = "urn:uuid:11111111-1111-1111-1111-11" + destNum
                            UserAgent = "IM-client/OMA1.0 moto/XT1033-4.4.2 DTAG/RCSEAndr-9.99-B9556-debug Orange-RCS/v2.5.18.r553"
                        feature_tags = 'expires=\\"3600\\";+g.3gpp.smsip;audio;+sip.instance=\\"' + sip_instance \
                                       + '\\"' + FEATURES + 'q=\\"1.0\\"'
                        contact = contact + '{\r\n"id":"' + str(j) + '",\r\n"RecRegTime":"' + str(int(time.time())-100+j) \
                                  + '",\r\n"sip_uri":"sip:' + destNum + "@" + ipv6_addr + ":" + port_num + '",\r\n' \
                                  + '"sip_instance":"' + sip_instance + '",\r\n' \
                                  + '"SuppFork":"1",\r\n' \
                                  + '"Contact_Expires":"3600",\r\n' \
                                  + '"UserAgent":"' + UserAgent + '",\r\n' \
                                  + '"feature_tags":"' + feature_tags + '"\r\n},'
                    contact = contact[:-1]
                    tp_data_base64 = convert_to_base64(tp_data + contact + '\r\n]\r\n}\r\n}}')
                    response_final = '{"rsp": {"regData": [{"versionNum": "1", "destUserId": "1' + destNum \
                                    + '", "tpDataType": "base64", "tpData": "' + tp_data_base64 \
                                    + '", "regInfoTTL": "3600", "expireFlag": "false", "nodeType": "RCS"}]}}'
                    GET_200 += 1
                    return web.Response(status=200, body=response_final, content_type='application/json')
            else:
                continue
        GET_404 += 1
        return web.Response(status=404)
    else:
        print("Dest num not found")

async def handle_store(request):
    global display_task_started, POST_201
    response_data = '{"rsp":{"rspText": "Successful created Reg Info"}}'
    POST_201 += 1
    return web.Response(status=201, body=response_data, content_type='application/json')

async def handle_update(request):
    global display_task_started, UPDATE_200
    response_data = '{"rsp":{"rspText": "Successful updated Reg Info"}}'
    UPDATE_200 += 1
    return web.Response(status=200, body=response_data, content_type='application/json')

async def handle_delete(request):
    global DELETE_200, reg_dereg_dict
    DELETE_200 += 1
    return web.Response(status=200, content_type='application/json')

app = web.Application()
app.add_routes([web.get('/scxml/nms/v1/Registration/{info}', handle_get),
                web.post('/scxml/nms/v1/Registration/update', handle_update),
                web.post('/scxml/nms/v1/Registration/store', handle_store),
                web.delete('/scxml/nms/v1/Registration/{info}', handle_delete)])
web.run_app(app, host=LOCAL_HOST, port=LOCAL_PORT)
