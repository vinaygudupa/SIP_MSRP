from aiohttp import web
from re import findall
from asyncio import sleep
import asyncio
import base64
import async_timeout
from random import randint
import time

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()

LOCAL_HOST = file_lines[0].split('=')[1].strip()
LOCAL_PORT = int(file_lines[1].split('=')[1].strip())
REMOTE_HOST = file_lines[2].split('=')[1].strip()
REMOTE_PORT = int(file_lines[3].split('=')[1].strip())
NUM_OF_MSRP_EXPECTED_IN_SESSION_CHAT = int(file_lines[4].split('=')[1].strip())
Number_range_with_stored_messages_starts_with = file_lines[5].split('=')[1].strip()
GroupChatNumRange = file_lines[6].split('=')[1].strip()
TIMEOUT = int(file_lines[7].split('=')[1].strip())

Group_Chat_range = GroupChatNumRange.split('-')

for i in range(len(Group_Chat_range)):
    Group_Chat_range[i] = Group_Chat_range[i][1:]

POST_Store_GC_part_info = 0
POST_Store_GC_sess_info = 0
POST_Store_GC_update_part_info = 0
POST_Store_GC_update_sess_info = 0
POST_Store_GC_MSRP_info = 0
POST_Store_Update = 0

GET_Session_NoRespNeeded = 0
GET_Session_GC = 0

POST_Session_GC = 0

GET_GC_Part_Info = 0
GET_GC_MSRP = 0

DELETE_MSRP_Chat = 0

DELETE_GC_Session = 0

display_task_started = False

def convert_to_base64(x):
    return str(base64.b64encode(x.encode()).decode())

async def send_packet_search_with_separator(reader, writer, packet, separator_1, search_string):
    try:
        async with async_timeout.timeout(TIMEOUT):
            writer.write(packet)
            await writer.drain()
        async with async_timeout.timeout(TIMEOUT):
            http_response = await reader.readuntil(separator=separator_1)
        if search_string in http_response:
            return True
        else:
            return False
    except asyncio.TimeoutError:
        return True
    except Exception as e:
        return False

async def POST_SESSION(call_type, dest_user_num):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global POST_Session_GC
    orignum = "22" + dest_user_num[2:10]
    dest_num_1 = "45" + dest_user_num[2:10]
    dest_num_2 = "46" + dest_user_num[2:10]
    dest_num_3 = "47" + dest_user_num[2:10]
    dest_num_4 = "48" + dest_user_num[2:10]
    dest_num_5 = "49" + dest_user_num[2:10]
    tp_data = '{'\
        '"req":'\
            '{'\
                '"initiatorContact":"' + convert_to_base64("sip:+1" + orignum + "@rcse-dls-capacity.mavenir.lab") + '",'\
                '"Contribution-Id":"GC-FWD-Conversation-' + orignum + '",' \
                '"gcFocusUri":"sip:1' + dest_user_num + '-ffffff11~sip%3Amavcid-1' + orignum + '-f2~0d31e37124459733cee5cfa9c88cc558%40rcse-dls-capacity.mavenir.lab%3A5060%3Btransport%3Dudp@rcse-dls-capacity.mavenir.lab:5060",' \
                '"ParticipantList":'\
                '[' \
                    '{' \
                        '"status":"active",' \
                        '"isCreator":0,' \
                        '"participantUri":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab"' \
                    '},' \
                    '{' \
                        '"status":"active",' \
                        '"isCreator":0,' \
                        '"participantUri":"sip:+1' + dest_num_1 + '@rcse-dls-capacity.mavenir.lab"' \
                    '},' \
                    '{' \
                        '"status":"active",' \
                        '"isCreator":0,' \
                        '"participantUri":"sip:+1' + dest_num_2 + '@rcse-dls-capacity.mavenir.lab"' \
                    '},' \
                    '{' \
                         '"status":"active",' \
                         '"isCreator":0,' \
                         '"participantUri":"sip:+1' + dest_num_3 + '@rcse-dls-capacity.mavenir.lab"' \
                    '},' \
                    '{' \
                        '"status":"active",' \
                        '"isCreator":0,' \
                        '"participantUri":"sip:+1' + dest_num_4 + '@rcse-dls-capacity.mavenir.lab"' \
                    '},' \
                    '{' \
                        '"status":"active",' \
                        '"isCreator":0,' \
                        '"participantUri":"sip:+1' + dest_num_5 + '@rcse-dls-capacity.mavenir.lab"' \
                    '},' \
                    '{' \
                        '"status":"active",' \
                        '"isCreator":1,' \
                        '"participantUri":"sip:+1' + orignum + '@rcse-dls-capacity.mavenir.lab"' \
                    '}' \
                '],'\
                '"SessionInfo":'\
                '{'\
                    '"From":"' + convert_to_base64("sip:+1" + orignum + "@rcse-dls-capacity.mavenir.lab") + ';;",'\
                    '"To":"sip:+1' + dest_user_num +'@rcse-dls-capacity.mavenir.lab",' \
                    '"Contact":"sip:1' + dest_user_num + '-ffffff11~sip%3Amavcid-1' + orignum + '-f2~0d31e37124459733cee5cfa9c88cc558%40rcse-dls-capacity.mavenir.lab%3A5060%3Btransport%3Dudp@rcse-dls-capacity.mavenir.lab:5060",' \
                    '"PAssertedID":"' + convert_to_base64("sip:+1" + orignum + "@rcse-dls-capacity.mavenir.lab") + ';;",'\
                    '"RequestURI":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'\
                    '"Subject":"",'\
                    '"Date":"",'\
                    '"Accept-Contact":"*;+g.3gpp.icsi-ref=' + "'urn%3Aurn-7%3A3gpp-service.ims.icsi.oma.cpm.session'" + ';explicit;require",'\
                    '"Referred-By":"' + convert_to_base64("sip:+1" + orignum + "@rcse-dls-capacity.mavenir.lab") + ';;",'\
                    '"imdnRequested":0,'\
                    '"retryCount":0,'\
                    '"Content-Type":"",'\
                    '"DestSubId":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",' \
                    '"msisdn":"+1' + dest_user_num + '",' \
                    '"sessStoreType":1,'\
                    '"sessionType":1'\
                '}'\
            '}'\
    '}'
    tp_data_base64 = convert_to_base64(tp_data)
    resp = '{' \
        '"rsp":{' \
            '"grpPartSessInfo":{'\
                '"sessInfoList":['\
                    '{'\
                        '"sessionInfo": {'\
                            '"conversationId":"GC-FWD-Conversation-' + orignum + '",'\
                            '"gcFocusUri":"sip:1' + dest_user_num + '-ffffff11~sip%3Amavcid-1' + orignum + '-f2~0d31e37124459733cee5cfa9c88cc558%40rcse-dls-capacity.mavenir.lab%3A5060%3Btransport%3Dudp@rcse-dls-capacity.mavenir.lab:5060",'\
                            '"participantFocusUri":"sip:1' + dest_user_num + '-ffffff11~sip%3Amavcid-1' + orignum + '-f2~0d31e37124459733cee5cfa9c88cc558%40rcse-dls-capacity.mavenir.lab%3A5060%3Btransport%3Dudp@rcse-dls-capacity.mavenir.lab:5060",'\
                            '"participantUri":"+1' + dest_user_num + '",'\
                            '"participantMsisdn":"+1' + dest_user_num + '",'\
                            '"initiatorContact":"' + convert_to_base64("sip:+1" + orignum + "@rcse-dls-capacity.mavenir.lab") + '",'\
                            '"tpData":"' + tp_data_base64 + '",'\
                            '"creationTimeStamp":"' + str(int(time.time())-100) + '",'\
                            '"tpDataType":"base64",'\
                            '"errorCode":"default_retry"'\
                        '},'\
                        '"participantList": {'\
                            '"participant":['\
                                '{' \
                                    '"isCreator":false,'\
                                    '"participantUri":"+1' + dest_user_num + '",'\
                                    '"participantMsisdn":"+1' + dest_user_num + '"'\
                                '},'\
                                '{'\
                                    '"status":"active",'\
                                    '"isCreator":false,'\
                                    '"participantUri":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'\
                                    '"participantMsisdn":"sip:+1' + dest_user_num +'@rcse-dls-capacity.mavenir.lab"'\
                                '},' \
                                '{' \
                                    '"status":"active",' \
                                    '"isCreator":false,' \
                                    '"participantUri":"sip:+1' + dest_num_1 + '@rcse-dls-capacity.mavenir.lab",' \
                                    '"participantMsisdn":"sip:+1' + dest_num_1 + '@rcse-dls-capacity.mavenir.lab"' \
                                '},'\
                                '{' \
                                    '"status":"active",' \
                                    '"isCreator":false,' \
                                    '"participantUri":"sip:+1' + dest_num_2 + '@rcse-dls-capacity.mavenir.lab",' \
                                    '"participantMsisdn":"sip:+1' + dest_num_2 + '@rcse-dls-capacity.mavenir.lab"' \
                                '},' \
                                '{' \
                                     '"status":"active",' \
                                     '"isCreator":false,' \
                                     '"participantUri":"sip:+1' + dest_num_3 + '@rcse-dls-capacity.mavenir.lab",' \
                                     '"participantMsisdn":"sip:+1' + dest_num_3 + '@rcse-dls-capacity.mavenir.lab"' \
                                '},' \
                                '{' \
                                      '"status":"active",' \
                                      '"isCreator":false,' \
                                      '"participantUri":"sip:+1' + dest_num_4 + '@rcse-dls-capacity.mavenir.lab",' \
                                      '"participantMsisdn":"sip:+1' + dest_num_4 + '@rcse-dls-capacity.mavenir.lab"' \
                                '},' \
                                '{' \
                                      '"status":"active",' \
                                      '"isCreator":false,' \
                                      '"participantUri":"sip:+1' + dest_num_5 + '@rcse-dls-capacity.mavenir.lab",' \
                                      '"participantMsisdn":"sip:+1' + dest_num_5 + '@rcse-dls-capacity.mavenir.lab"' \
                                '},' \
                                '{' \
                                       '"status":"active",' \
                                       '"isCreator":true,' \
                                       '"participantUri":"sip:+1' + orignum + '@rcse-dls-capacity.mavenir.lab",' \
                                       '"participantMsisdn":"sip:+1' + orignum + '@rcse-dls-capacity.mavenir.lab"' \
                                '}' \
                            ']'\
                        '}'\
                    '}'\
                ']'\
            '}'\
        '}'\
    '}'
    post_initial_data = 'POST /mstoreproxy/v1/SF/forward/IM?type=gcImSessInfo HTTP/1.1\r\n' \
                        'Host: sfmstore.mavenir.lab:8081\r\n' \
                        'Content-Type: application/json\r\n' \
                        'Connection: Close\r\n' \
                        'Accept:application/json\r\n' \
                        'x-anchor-id:+1' + dest_user_num +'\r\n'\
                        'Content-Length: ' + str(len(resp)) + '\r\n\r\n'

    HTTP_response = post_initial_data + resp

    try:
        async with async_timeout.timeout(TIMEOUT):
            reader_1, writer_1 = await asyncio.open_connection(host=REMOTE_HOST, port=REMOTE_PORT)
            result = await send_packet_search_with_separator(reader_1, writer_1, HTTP_response.encode(), b'Server: Mavenir Web Application Server', b'200 OK')
            if result:
                if call_type == 'GC':
                    POST_Session_GC += 1
                else:
                    print("POST session failed")
    except asyncio.TimeoutError:
        print("POST session Exception")


async def handle_post_store(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global POST_Store_GC_part_info, POST_Store_GC_sess_info, POST_Store_GC_update_part_info, POST_Store_GC_MSRP_info
    global POST_Store_GC_update_sess_info, POST_Store_Update
    req_url = str(request.url)
    status_code = 200
    if 'gcCreateGroupPartInfo' in req_url:
        await sleep(0.2)
        POST_Store_GC_part_info += 1
        rsp_json = {"rsp":{"rspText":"Successful created Group Participant Info"}}
        status_code = 201
    elif 'gcCreateGroupPartSessInfo' in req_url:
        await sleep(0.2)
        POST_Store_GC_sess_info += 1
        rsp_json = {"rsp":{"rspText":"Successful created Group IM Participant and Session"}}
        status_code = 201
    elif 'updateGroupPartInfo' in req_url:
        await sleep(0.2)
        POST_Store_GC_update_part_info += 1
        rsp_json = {"rsp":{"rspText":"Successful update Group IM Participant Info"}}
        status_code = 200
    elif 'updateGcImSessInfo' in req_url:
        await sleep(0.2)
        POST_Store_GC_update_sess_info += 1
        rsp_json = {"rsp":{"rspText":"Successful update of Group IM Session"}}
        status_code = 200
    elif 'grpMsrpImData' in req_url:
        await sleep(0.2)
        POST_Store_GC_MSRP_info += 1
        rsp_json = {"rsp":{"rspText":"Successful created Group IM MSRP Data"}}
        status_code = 201
    elif 'update' in req_url:
        await sleep(0.2)
        POST_Store_Update += 1
        message_list = ''
        request_body = await request.read()
        message_id_list = findall(b'\{"messageId":"(.*?)","', request_body)
        for i in message_id_list:
            ok_status = '{"messageId":"' + str(i.decode()) + '","status":"200"}'
            message_list += ok_status + ','
        message_list = message_list[:-1]
        rsp_json = {"rsp":{"ResponseList":[message_list]}}
        status_code = 200
    else:
        rsp_json = ''
        status_code = 200
    return web.json_response(rsp_json, status=status_code)

async def handle_get_session(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global GET_Session_NoRespNeeded, GET_Session_GC
    req_url = str(request.url)
    destNum = findall(r'destUserId=\+1(\d{10})', req_url)
    if destNum:
        destNum = destNum[0]
        dest_num_int = int(destNum)
        if not destNum.startswith(Number_range_with_stored_messages_starts_with[1:]):
            GET_Session_NoRespNeeded += 1
        elif (dest_num_int >= int(Group_Chat_range[0]) and dest_num_int <= int(Group_Chat_range[1])):
            GET_Session_GC += 1
            app.loop.create_task(POST_SESSION('GC', destNum))
    else:
        print("Dest_Num not found in GET_Session packet.")
    return web.Response()

async def handle_get_part_info(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global GET_GC_Part_Info, GET_GC_MSRP
    req_url = str(request.url)
    if 'getPartListInfo' in req_url:
        dest_user_num = findall(r'destUserId=1(\d{10})', req_url)[0]
        convertaionID = findall(r'conversationId=(.*?)&RmsType=On', req_url)[0]
        orignum = "22" + dest_user_num[2:10]
        dest_num_1 = "45" + dest_user_num[2:10]
        dest_num_2 = "46" + dest_user_num[2:10]
        dest_num_3 = "47" + dest_user_num[2:10]
        dest_num_4 = "48" + dest_user_num[2:10]
        dest_num_5 = "49" + dest_user_num[2:10]
        rsp_json = '{'\
            '"rsp": {'\
                '"attributeList": {'\
                    '"initiatorContact": "<sip:mavodi-0-cd-0-1-ffffff20-sip%3A%2B1' + orignum + '-641@rcse-dls-capacity.mavenir.lab:5060;transport=udp>",' \
                    '"gcFocusUri":"sip:mavcid-1' + orignum + '-f2~0d31e37124459733cee5cfa9c88cc558@rcse-dls-capacity.mavenir.lab:5060",' \
                    '"contributionId":"' + convertaionID + '",'\
                    '"conversationId":"' + convertaionID + '",' \
                    '"groupType":"open"'\
                '},'\
                '"participantList":{'\
                    '"participant":[ '\
                        '{' \
                            '"status": "booted",'\
                            '"isCreator":false,'\
                            '"participantUri":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",' \
                            '"roleType":"Normal",'\
                            '"participantMsisdn":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab"'\
                        '},' \
                        '{' \
                            '"status": "booted",' \
                            '"isCreator":false,' \
                            '"participantUri":"sip:+1' + dest_num_1 + '@rcse-dls-capacity.mavenir.lab",' \
                            '"roleType":"Normal",' \
                            '"participantMsisdn":"sip:+1' + dest_num_1 + '@rcse-dls-capacity.mavenir.lab"' \
                        '},' \
                        '{' \
                            '"status": "booted",' \
                            '"isCreator":false,' \
                            '"participantUri":"sip:+1' + dest_num_2 + '@rcse-dls-capacity.mavenir.lab",' \
                            '"roleType":"Normal",' \
                            '"participantMsisdn":"sip:+1' + dest_num_2 + '@rcse-dls-capacity.mavenir.lab"' \
                        '},' \
                        '{' \
                            '"status": "booted",' \
                            '"isCreator":false,' \
                            '"participantUri":"sip:+1' + dest_num_3 + '@rcse-dls-capacity.mavenir.lab",' \
                            '"roleType":"Normal",' \
                            '"participantMsisdn":"sip:+1' + dest_num_3 + '@rcse-dls-capacity.mavenir.lab"' \
                        '},' \
                        '{' \
                            '"status": "booted",' \
                            '"isCreator":false,' \
                            '"participantUri":"sip:+1' + dest_num_4 + '@rcse-dls-capacity.mavenir.lab",' \
                            '"roleType":"Normal",' \
                            '"participantMsisdn":"sip:+1' + dest_num_4 + '@rcse-dls-capacity.mavenir.lab"' \
                        '},' \
                        '{' \
                            '"status": "booted",' \
                            '"isCreator":false,' \
                            '"participantUri":"sip:+1' + dest_num_5 + '@rcse-dls-capacity.mavenir.lab",' \
                            '"roleType":"Normal",' \
                            '"participantMsisdn":"sip:+1' + dest_num_5 + '@rcse-dls-capacity.mavenir.lab"' \
                        '},' \
                        '{' \
                        '"status": "booted",' \
                        '"isCreator":true,' \
                        '"participantUri":"sip:+1' + orignum + '@rcse-dls-capacity.mavenir.lab",' \
                        '"roleType":"Administrator",' \
                        '"participantMsisdn":"sip:+1' + orignum + '@rcse-dls-capacity.mavenir.lab"' \
                        '}' \
                    ']'\
                '}'\
            '}'\
        '}'
        try:
            GET_GC_Part_Info += 1
            return web.Response(body=rsp_json, content_type='application/json')
        except Exception as e:
            print("Exception: " + str(e))
    elif 'getGrpmsrpData' in req_url:
        req_url = str(request.url)
        destNum = findall(r'destUserId=\+1(\d{10})', req_url)[0]
        origNum = '22' + destNum[2:10]
        dest_num_int = int(destNum)
        GET_GC_MSRP += 1
        Content_Initial_part_1 = 'From: ' + origNum + '<sip:+1' + origNum + '@rcse-dls-capacity.mavenir.lab>\r\n' \
                                                                            'NS: imdn<urn:ietf:params:imdn>\r\n' \
                                                                            'imdn.Message-ID: mstore_imdn' + origNum + '-' + destNum
        Content_Initial_part_2 = '\r\nimdn.Disposition-Notification: positive-delivery, display\r\n' \
                                 'DateTime: 2018-02-28T15:17:33Z\r\n' \
                                 'To: <sip:+1' + destNum + '@rcse-dls-capacity.mavenir.lab>\r\n' \
                                                           '\r\n' \
                                                           'Content-type: text/plain\r\n ' \
                                                           'Content-length: 200\r\n\r\n'
        Content_Data = 'STORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHAT' \
                       'STORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATST'
        Content_data_last_part = Content_Initial_part_2 + Content_Data
        tp_data_initial = '{"req":{"SuccessReport":1,"FailureReport":1,"ContentDisposition":""' \
                          ',"ImdnRequested":1,"Content-Type":"message/cpim","Content":"'
        tp_data_last = '","CreateTime":"0","fksessionId":-1}}'
        data_to_send_in_200OK = '{"rsp":{"Messages":['
        for i in range(NUM_OF_MSRP_EXPECTED_IN_SESSION_CHAT):
            Content_X = Content_Initial_part_1 + "imdn" + str(i + 1) + Content_data_last_part
            tp_data_X = convert_to_base64(tp_data_initial + convert_to_base64(Content_X) + tp_data_last)
            message_X = '{"messageId":"' \
                        + str(randint(0000, 9999)) + str(randint(0000, 9999)) + '-5cba-149d-bb2c-35' \
                        + origNum + '","tpDataType":"base64","tpData":"' + tp_data_X + '"}'
            data_to_send_in_200OK += message_X + ','
        data_to_send_in_200OK = data_to_send_in_200OK[:-1]
        data_to_send_in_200OK += ']}}'
        return web.Response(body=data_to_send_in_200OK, content_type='application/json')


async def handle_delete_data(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global DELETE_MSRP_Chat
    http_body = await request.read()
    message_id_list = findall(b'\{"messageId":"(.*?)"\}', http_body)
    message_list = ''
    for i in message_id_list:
        ok_status = '{"messageId":"' + str(i.decode()) + '","status":"200"}'
        message_list += ok_status + ','
    message_list = message_list[:-1]
    http_resp_data = '{"rsp":{"ResponseList":[' + message_list + ']}}'
    DELETE_MSRP_Chat += 1
    return web.Response(body=http_resp_data, content_type='application/json')

async def handle_delete_session(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global DELETE_GC_Session
    DELETE_GC_Session += 1
    return web.Response(status=204)

async def display_count():
    print("Display coroutine started")
    while True:
        await sleep(5)
        print("################################################################")
        print("RECV_STORE_POST_Participant")
        print("   GC_PartInfo_create:  " + str(POST_Store_GC_part_info) +
              "   GC_PartInfoUpdate:  " + str(POST_Store_GC_update_part_info) +
              "   GC_Sess_create:  " + str(POST_Store_GC_sess_info) +
              "   GC_Sess_update:  " + str(POST_Store_GC_update_sess_info) +
              "   GC_MSRP_Create: " + str(POST_Store_GC_MSRP_info))
        print("RECV_GET_Session")
        print("   No_Rsp_Needed: " + str(GET_Session_NoRespNeeded) + 
              "   GC_Ssssion:  " + str(GET_Session_GC))
        print("SEND_POST_GC_Session")
        print("   GC_Session:  " + str(POST_Session_GC))
        print("GET DATA")
        print("    GC_Part_info:   " + str(GET_GC_Part_Info) +
              "    GC_MSRP:    " + str(GET_GC_MSRP))
        print("DELETE MSRP DATA")
        print("     DELETE_MSRP:   " + str(DELETE_MSRP_Chat))
        print("DELETE GC SESSION")
        print("     DELETE_GC_SESSION:   " + str(DELETE_GC_Session))

app = web.Application()
app.add_routes([web.post('/mStoreRoot/V1/SF/store/{info}', handle_post_store),
                web.get('/mStoreRoot/V1/SF/forward/{info}', handle_get_session),
                web.get('/mStoreRoot/V1/SF/retrieve/{info}', handle_get_part_info),
                web.post('/mStoreRoot/V1/SF/delete/{info}', handle_delete_data),
                web.delete('/mStoreRoot/V1/SF/delete/{info}', handle_delete_session)])
web.run_app(app, host=LOCAL_HOST, port=LOCAL_PORT)

