from aiohttp import web
from re import findall
from asyncio import sleep
import asyncio
import base64
import async_timeout
from random import randint

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()

LOCAL_HOST = file_lines[0].split('=')[1].strip()
LOCAL_PORT = int(file_lines[1].split('=')[1].strip())
REMOTE_HOST = file_lines[2].split('=')[1].strip()
REMOTE_PORT = int(file_lines[3].split('=')[1].strip())
NUM_OF_MSRP_EXPECTED_IN_SESSION_CHAT = int(file_lines[4].split('=')[1].strip())
FILE_NAME_BASE64_DATA = file_lines[5].split('=')[1].strip()
Number_range_with_stored_messages_starts_with = file_lines[6].split('=')[1].strip()
LM_SIZE = int(file_lines[7].split('=')[1].strip())
LM_NAME_BASE64_DATA = file_lines[8].split('=')[1].strip()
ChatNumRange = file_lines[9].split('=')[1].strip()
FTNumRange = file_lines[10].split('=')[1].strip()
PMNumRange = file_lines[11].split('=')[1].strip()
LMNumRange = file_lines[12].split('=')[1].strip()
HTTPFTNumRange = file_lines[13].split('=')[1].strip()
TIMEOUT = int(file_lines[14].split('=')[1].strip())

FILE_DATA_BASE64 = open(FILE_NAME_BASE64_DATA, 'rb').read()
LM_DATA_BASE64 = open(LM_NAME_BASE64_DATA, 'rb').read()

Chat_range = ChatNumRange.split('-')
FT_range = FTNumRange.split('-')
PM_range = PMNumRange.split('-')
LM_range = LMNumRange.split('-')
HTTP_FT_range = HTTPFTNumRange.split('-')

for i in range(0,len(Chat_range)):
    Chat_range[i] = Chat_range[i][1:]
    FT_range[i] = FT_range[i][1:]
    PM_range[i] = PM_range[i][1:]
    LM_range[i] = LM_range[i][1:]
    HTTP_FT_range[i] = HTTP_FT_range[i][1:]

POST_Store_Chat_Session = 0
POST_Store_Chat_MSRP = 0
POST_Store_FT_Session = 0
POST_Store_FT_MSRP = 0
POST_Store_PM = 0
POST_Store_LM_Session = 0
POST_Store_LM_MSRP = 0
POST_Store_GC_Session = 0
POST_Store_Update = 0

GET_Session_Chat = 0
GET_Session_FT = 0
GET_Session_PM = 0
GET_Session_LM = 0
GET_Session_HTTPFT = 0
GET_Session_NoRespNeeded = 0

POST_Session_Chat = 0
POST_Session_FT = 0
POST_Session_PM = 0
POST_Session_LM = 0
POST_Session_HTTPFT = 0

GET_MSRP_Chat = 0
GET_MSRP_FT = 0
GET_MSRP_LM = 0
GET_MSRP_HTTPFT = 0

DELETE_MSRP_Chat = 0
DELETE_PM = 0

DELETE_Session_Chat = 0
DELETE_FT = 0
DELETE_LM = 0

POST_SLASH = 0

display_task_started = False

def convert_to_base64(x):
    return base64.b64encode((x).encode())

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
    global POST_Session_Chat, POST_Session_FT, POST_Session_PM, POST_Session_LM, POST_Session_HTTPFT
    orignum = "22" + dest_user_num[2:10]
    sip_instance = "<urn:gsma:imei:" + orignum[0:8] + "-" + orignum[8:10] + "0000-0>"
    From_header = convert_to_base64("<sip:+1" + orignum + "@rcse-dls-capacity.mavenir.lab>")
    if call_type == 'CHAT':
        session_info_type = "imSessInfo"
        Contribution_id = 'STORE_FWD_Contribution-' + orignum
        ContentType = ""
        Extra = '"isUPTsmsFT":0,"isUPTsmsGEO":0,'
        sessStoreType = '1'
        message_id = '"messageId":"' + str(randint(11111111, 99999999)) + "-5cba-149d-bb2c-f" + str(
            randint(00000, 99999)) + '1d'
        rsp_data_begin_part = '{"rsp":{"subType":"ON","sessionInfoList":{"sessInfo":[{"origUserId":"+1' + orignum + '","destUserId":"+1' + dest_user_num + '","tpData":"'
        rsp_data_end = '","tpDataType":"base64",' + message_id + '","errorCode":"default_retry"}]}}}'
        Contact_header = '<sip:mavodi-0-cd-0-1-' + str(
            randint(00000000, 99999999)) + '-@rcse-dls-capacity.mavenir.lab:5060;transport=tcp>;' \
                                           '+sip.instance="' + sip_instance + '";+g.3gpp.icsi-ref="urn%3Aurn-7%3A3gpp-service.ims.icsi.oma.cpm.session"'
        Contact_header = convert_to_base64(Contact_header)
        tp_data_from = '"From":"' + str(From_header.decode()) + '",'
        tp_data_to = '"To":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_destsub_id = '"DestSubscriberId": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_passert_id = '"PAssertedId": "' + str(From_header.decode()) + '",'
        tp_data_req_id = '"RequestURI": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_contact = '"Contact": "' + str(
            Contact_header.decode()) + '","Subject":"","Date": "Mon, 26 Sep 2011 10:30:01 GMT",' \
                          + '"Accept-Contact":"*;+g.3gpp.icsi-ref=' + "'" + 'urn%3Aurn-7%3A3gpp-service.ims.icsi.oma.cpm.session' + "'" + ';explicit;require",'
        tp_data_referred_by = '"Referred-By":"",'
        tp_data_contribution_id = '"Contribution-Id":"' + str(Contribution_id) + '",' + Extra
        tp_data_type = '"Content-Type":"' + ContentType + '","InitialContent":"","ImdnRequested":0,"retryCount":0,"CreateTime":"2018-03-08T06:32:37.690Z","isOrig":0,"msisdn":"1' + dest_user_num + '",'
        tp_data_session_type = '"sessStoreType":' + sessStoreType + ',"sessionType":2,"isDelayIw":0,"validityTime":0,"callType":509245066,"FromMsisdn":"1' + str(
            orignum) + '"'
        tp_data_full = '{"req":{' + tp_data_from + tp_data_to + tp_data_destsub_id + tp_data_passert_id + tp_data_req_id + tp_data_contact \
                       + tp_data_referred_by + tp_data_contribution_id + tp_data_type + tp_data_session_type + '}}'
        tp_data_base64 = convert_to_base64(tp_data_full)
        rsp_data_begin = rsp_data_begin_part + str(tp_data_base64.decode())
        rsp_data = rsp_data_begin + rsp_data_end
        POST_fixed_data = 'POST /mstoreproxy/v1/SF/forward/IM?type=' + session_info_type + ' HTTP/1.1\r\n' \
                          'Host: mstorestoreforward.mavenir.lab:8081\r\n' \
                          'Content-Type: application/json\r\n' \
                          'Accept:application/json\r\n' \
                          'Content-Length: '
    elif call_type == 'FT':
        Contribution_id = 'STORE-FWD-FT-Contribution-' + orignum
        tp_data_from = '"From": "' + str(From_header.decode()) + ';;",'
        tp_data_to = '"To":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_destsub_id = '"DestSubscriberId": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_passert_id = '"PAssertedId": "' + str(From_header.decode()) + ';;",'
        tp_data_req_id = '"RequestURI": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_contact = '"Contact": "sip:mavodi-0-cd-0-2-' + str(
            randint(00000000, 99999999)) + '-@rcse-dls-capacity.mavenir.lab:5060",'
        tp_data_fixed_1 = '"Subject": "","Date": "","Accept-Contact": "*;+g.3gpp.icsi-ref=' + "'urn%3Aurn-7%3A3gpp-service.ims.icsi.oma.cpm.filetransfer'" + ';explicit;require","Referred-By": "",'
        tp_data_contribution_id = '"Contribution-Id":"' + str(Contribution_id) + '",'
        tp_data_fixed_2 = '"Content-Type":"message/cpim","Content-Disposition": "","ImdnRequested": 0,"retryCount": 0,"SuccessReport": 0,"FailureReport": 1,"isOrig": 0,'
        tp_data_fileselector = '"FileSelector":"name:' + "'" + str(orignum) + '.jpeg' + "'" + 'type:image/jpeg size:2625197 ",'
        tp_data_fixed_3 = '"Cpim_content": "","Thumbnail": "",'
        tp_data_msisdn = '"msisdn": "' + dest_user_num + '","sessStoreType": 2,"sessionType": 2'
        tp_data_full = '{"req": {' + tp_data_from + tp_data_to + tp_data_destsub_id + tp_data_passert_id + tp_data_req_id \
                       + tp_data_contact + tp_data_fixed_1 + tp_data_contribution_id + tp_data_fixed_2 + tp_data_fileselector + tp_data_fixed_3 + tp_data_msisdn + '}}'
        tp_data_base64 = convert_to_base64(tp_data_full)
        rsp_data = '{"rsp": {"subType": "ON","fileSessInfoList": {"fileSessInfo": [{"origUserId": "sip:+1' + str(orignum) + '@rcse-dls-capacity.mavenir.lab","destUserId":' \
                       ' "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab","tpData": "' + str(tp_data_base64.decode()) + '","tpDataType": "base64","fileIdentifier":' \
                                       ' "dc1b4710-62c4-13e2-' + str(randint(0000, 9999)) + '-e36b9b42' + str(randint(0000, 9999)) + '","swiftUri": "/v1/AUTH_TMO_Raj_1/' \
                                   'CONT_1/dc1b4710-62c4-13e2-b857-e36b9b4235f3_2' + str(randint(000000000000, 999999999999)) + '","expireFlag": false}]}}}'
        POST_fixed_data = 'POST /mstoreproxy/v1/SF/forward/IM?type=ftSessInfo HTTP/1.1\r\n' \
                          'Host: mstorestoreforward.mavenir.lab:8081\r\n' \
                          'Content-Type: application/json\r\n' \
                          'x-anchor-id:sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab\r\n' \
                          'Accept:application/json\r\n' \
                          'Content-Length: '
    elif call_type == 'PM':
        tp_data_from = '"From": "<sip:+1' + str(orignum) + '@rcse-dls-capacity.mavenir.lab>",'
        tp_data_to = '"To": "<sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab>",'
        tp_data_passert_id = '"PAssertedID": "<sip:+1' + str(orignum) + '@rcse-dls-capacity.mavenir.lab>",'
        tp_data_req_id = '"RequestURI": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_Contribution_id = '"Contribution-Id":"STORE-FWD-PM-Contribution-' + orignum + '",'
        tp_data_contact = '"Contact": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_contentDisposition = '"Content-Disposition": "","Content-Type":"message/cpim",'
        tp_destSubId = '"DestSubID": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        Actual_Content = 'From: +1' + str(orignum) + ' <sip:+1' + str(orignum) + '@rcse-dls-capacity.mavenir.lab>\r\n' \
                         + 'To: +1' + dest_user_num + ' <sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab>\r\n' \
                         + 'NS: imdn<urn:ietf:params:imdn>\r\n' \
                         + 'imdn.Message-ID: PMIMDNSF' + str(randint(000000, 999999)) + '\r\n' \
                         + 'DateTime: 2018-02-16T01:42:50+5:30\r\nimdn.Disposition-Notification: positive-delivery, display\r\n\r\n' \
                         + 'Content-Type: text/plain\r\nContent-Length: 200\r\n\r\n' \
                         + 'STORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHAT' \
                           'STORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATSTORE_AND_FORWARD_CHATST'
        tp_content = '"Content": "' + str(convert_to_base64(Actual_Content).decode()) + '",'
        tp_msisdn = '"msisdn": "' + dest_user_num + '",'
        tp_Conversation_id = '"conversationId": "STORE-FWD-PM-Conversation-' + orignum + '",'
        tp_MessageSesssionType = '"MessageSessionType": 2,'
        tp_accept_contact = '"Accept-Contact": "KjsrZy4zZ3BwLmljc2ktcmVmPSJ1cm4lM0F1cm4tNyUzQTNncHAtc2VydmljZS5pbXMuaWNzaS5vbWEuY3BtLm1zZyI="'

        tp_data = '{"req": {' + tp_data_from + tp_data_to + tp_data_passert_id + tp_data_req_id + tp_Contribution_id + tp_data_contact + tp_contentDisposition \
                  + tp_destSubId + tp_content + tp_msisdn + tp_Conversation_id + tp_MessageSesssionType + tp_accept_contact + '}}'
        tp_data_base64 = convert_to_base64(tp_data)
        rsp_data = '{"rsp":{"Messages":[{"origUserId":"sip:+1' + str(orignum) + '@rcse-dls-capacity.mavenir.lab","destUserId":"sip:+1' + dest_user_num \
                   + '@rcse-dls-capacity.mavenir.lab","messageId":"' + str(randint(00000000, 99999999)) + '-5ae3-13e2-a340-e36b9b4235f2","tpDataType":"base64Encode","tpData":"' \
                   + str(tp_data_base64.decode()) + '"}],"subType":"OFF"}}'
        POST_fixed_data = 'POST /mstoreproxy/v1/SF/forward/IM?type=pageModeMsg HTTP/1.1\r\n' \
                          'Host: mstorestoreforward.mavenir.lab:8081\r\n' \
                          'Content-Type: application/json\r\n' \
                          'x-anchor-id:sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab\r\n' \
                          'Accept:application/json\r\n' \
                          'Content-Length: '
    elif call_type == 'LM':
        Contribution_id = 'STORE_FWD_LM_Contribution-' + orignum
        tp_data_from = '"From": "' + str(From_header.decode()) + ';;",'
        tp_data_to = '"To":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_destsub_id = '"DestSubscriberId": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_passert_id = '"PAssertedId": "' + str(From_header.decode()) + ';;",'
        tp_data_req_id = '"RequestURI": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_contact = '"Contact": "sip:mavodi-0-cd-0-2-' + str(
            randint(00000000, 99999999)) + '-@rcse-dls-capacity.mavenir.lab:5060",'
        tp_data_fixed_1 = '"Subject": "","Date": "","Accept-Contact": "*;+g.3gpp.icsi-ref=' + "'urn%3Aurn-7%3A3gpp-service.ims.icsi.oma.cpm.largemsg'" + ';explicit;require","Referred-By": "",'
        tp_data_contribution_id = '"Contribution-Id":"' + str(Contribution_id) + '",'
        tp_data_fixed_2 = '"Content-Type":"message/cpim","Content-Disposition": "","ImdnRequested": 0,"retryCount": 0,"SuccessReport": 0,"FailureReport": 1,"isOrig": 0,'
        tp_data_fileselector = '"FileSelector":"size:' + str(LM_SIZE) + ' ",'
        tp_data_fixed_3 = '"Cpim_content": "","Thumbnail": "",'
        tp_data_msisdn = '"msisdn": "' + dest_user_num + '","sessStoreType": 2,"sessionType": 2,'
        tp_data_conversation_id = '"conversationId":"STORE_FWD_LM_Conversation-' + str(orignum) + '"'
        tp_data_full = '{"req": {' + tp_data_from + tp_data_to + tp_data_destsub_id + tp_data_passert_id + tp_data_req_id \
                       + tp_data_contact + tp_data_fixed_1 + tp_data_contribution_id + tp_data_fixed_2 + tp_data_fileselector + tp_data_fixed_3 + tp_data_msisdn + tp_data_conversation_id + '}}'
        tp_data_base64 = convert_to_base64(tp_data_full)
        rsp_data = '{"rsp": {"subType": "ON","fileSessInfoList": {"fileSessInfo": [{"origUserId": "sip:+1' + str(
            orignum) + '@rcse-dls-capacity.mavenir.lab","destUserId":' \
                       ' "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab","tpData": "' + str(
            tp_data_base64.decode()) + '","tpDataType": "base64","fileIdentifier":' \
                                       ' "dc1b4710-62c4-11e1-' + str(randint(0000, 9999)) + '-e36b9b42' + str(
            randint(0000, 9999)) + '","swiftUri": "/v1/AUTH_TMO_Raj_1/' \
                                   'CONT_1/dc1b4710-62c4-13e2-b857-e36b9b4235f2_1' + str(
            randint(000000000000, 999999999999)) + '","expireFlag": false}]}}}'
        POST_fixed_data = 'POST /mstoreproxy/v1/SF/forward/Message?type=lmSessInfo HTTP/1.1\r\n' \
                          'Host: mstorestoreforward.mavenir.lab:8081\r\n' \
                          'Content-Type: application/json\r\n' \
                          'x-anchor-id:sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab\r\n' \
                          'Accept:application/json\r\n' \
                          'Content-Length: '
    elif call_type == 'HTTPFT':
        session_info_type = "imSessInfo"
        Contribution_id = 'STORE_FWD_HTTPFT_Contribution-' + orignum
        ContentType = ""
        Extra = '"isUPTsmsFT":0,"isUPTsmsGEO":0,'
        sessStoreType = '1'
        message_id = '"messageId":"' + str(randint(11111111, 99999999)) + "-5cba-149d-bb2c-f" + str(
            randint(00000, 99999)) + '1d'
        rsp_data_begin_part = '{"rsp":{"subType":"ON","sessionInfoList":{"sessInfo":[{"origUserId":"+1' + orignum + '","destUserId":"+1' + dest_user_num + '","tpData":"'
        rsp_data_end = '","tpDataType":"base64",' + message_id + '","errorCode":"default_retry"}]}}}'
        POST_fixed_data = 'POST /mstoreproxy/v1/SF/forward/IM?type=' + session_info_type + ' HTTP/1.1\r\n' \
                                                                                           'Host: mstorestoreforward.mavenir.lab:8081\r\n' \
                                                                                           'Content-Type: application/json\r\n' \
                                                                                           'Accept:application/json\r\n' \
                                                                                           'Content-Length: '
        Contact_header = '<sip:mavodi-0-cd-0-1-' + str(
            randint(00000000, 99999999)) + '-@rcse-dls-capacity.mavenir.lab:5060;transport=tcp>;' \
                                           '+sip.instance="' + sip_instance + '";+g.3gpp.icsi-ref="urn%3Aurn-7%3A3gpp-service.ims.icsi.oma.cpm.session"'
        Contact_header = convert_to_base64(Contact_header)
        tp_data_from = '"From":"' + str(From_header.decode()) + '",'
        tp_data_to = '"To":"sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_destsub_id = '"DestSubscriberId": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_passert_id = '"PAssertedId": "' + str(From_header.decode()) + '",'
        tp_data_req_id = '"RequestURI": "sip:+1' + dest_user_num + '@rcse-dls-capacity.mavenir.lab",'
        tp_data_contact = '"Contact": "' + str(
            Contact_header.decode()) + '","Subject":"","Date": "Mon, 26 Sep 2011 10:30:01 GMT",' \
                          + '"Accept-Contact":"*;+g.3gpp.icsi-ref=' + "'" + 'urn%3Aurn-7%3A3gpp-service.ims.icsi.oma.cpm.session' + "'" + ';explicit;require",'
        tp_data_referred_by = '"Referred-By":"",'
        tp_data_contribution_id = '"Contribution-Id":"' + str(Contribution_id) + '",' + Extra
        tp_data_type = '"Content-Type":"' + ContentType + '","InitialContent":"","ImdnRequested":0,"retryCount":0,"CreateTime":"2018-03-08T06:32:37.690Z","isOrig":0,"msisdn":"1' + dest_user_num + '",'
        tp_data_session_type = '"sessStoreType":' + sessStoreType + ',"sessionType":2,"isDelayIw":0,"validityTime":0,"callType":509245066,"FromMsisdn":"1' + str(
            orignum) + '"'
        tp_data_full = '{"req":{' + tp_data_from + tp_data_to + tp_data_destsub_id + tp_data_passert_id + tp_data_req_id + tp_data_contact \
                       + tp_data_referred_by + tp_data_contribution_id + tp_data_type + tp_data_session_type + '}}'
        tp_data_base64 = convert_to_base64(tp_data_full)
        rsp_data_begin = rsp_data_begin_part + str(tp_data_base64.decode())
        rsp_data = rsp_data_begin + rsp_data_end
    len_data = len(rsp_data)
    HTTP_response = POST_fixed_data + str(len_data) + '\r\n\r\n' + rsp_data
    try:
        async with async_timeout.timeout(TIMEOUT):
            reader_1, writer_1 = await asyncio.open_connection(host=REMOTE_HOST, port=REMOTE_PORT)
            result = await send_packet_search_with_separator(reader_1, writer_1, HTTP_response.encode(), b'Server: Mavenir Web Application Server', b'200 OK')
            if result:
                if call_type == 'CHAT':
                    POST_Session_Chat += 1
                elif call_type == 'FT':
                    POST_Session_FT += 1
                elif call_type == 'PM':
                    POST_Session_PM += 1
                elif call_type == 'LM':
                    POST_Session_LM += 1
                elif call_type == 'HTTPFT':
                    POST_Session_HTTPFT += 1
                else:
                    print("POST session failed")
    except asyncio.TimeoutError:
        print("POST session Exception")

async def handle_post_store(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global POST_Store_Chat_Session, POST_Store_Chat_MSRP, POST_Store_FT_Session, POST_Store_FT_MSRP
    global POST_Store_PM, POST_Store_LM_Session, POST_Store_LM_MSRP, POST_Store_GC_Session, POST_Store_Update
    req_url = str(request.url)
    if 'imSessInfo' in req_url:
        await sleep(0.2)
        POST_Store_Chat_Session += 1
        rsp_json = {"rsp":{"rspText":"Successfully created IM Session"}}
    elif 'msrpImData' in req_url:
        await sleep(0.2)
        POST_Store_Chat_MSRP += 1
        rsp_json = {"rsp":{"rspText":"Successful created IM MSRP Data"}}
    elif 'ftImSessInfo' in req_url:
        await sleep(0.2)
        POST_Store_FT_Session += 1
        rsp_json = {"rsp":{"rspText":"Successfully created FT Session"}}
    elif 'ftData' in req_url:
        await sleep(0.5)
        POST_Store_FT_MSRP += 1
        rsp_json = {"rsp":{"rspText":"Successful created IM FT Data"}}
    elif 'pageModeMsg' in req_url:
        await sleep(0.2)
        POST_Store_PM += 1
        rsp_json = {"rsp":{"rspText":"Successful created PM Message"}}
    elif 'lmSessInfo' in req_url:
        await sleep(0.2)
        POST_Store_LM_Session += 1
        rsp_json = {"rsp":{"rspText":"Successful created LM Message"}}
    elif 'lmData' in req_url:
        await sleep(0.5)
        POST_Store_LM_MSRP += 1
        rsp_json = {"rsp":{"rspText":"Successful created LM Data"}}
    elif 'GC' in req_url:
        await sleep(0.2)
        POST_Store_GC_Session += 1
        rsp_json = {"rsp":{"rspText":"Successful created GC Data"}}
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
    else:
        rsp_json = ''
    return web.json_response(rsp_json, status=201)

async def handle_get_session(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global GET_Session_Chat, GET_Session_FT, GET_Session_PM, GET_Session_LM
    global GET_Session_HTTPFT, GET_Session_NoRespNeeded
    req_url = str(request.url)
    destNum = findall(r'destUserId=\+1(\d{10})', req_url)
    if destNum:
        destNum = destNum[0]
        dest_num_int = int(destNum)
        if not destNum.startswith(Number_range_with_stored_messages_starts_with[1:]):
            GET_Session_NoRespNeeded += 1
        elif (dest_num_int >= int(Chat_range[0]) and dest_num_int <= int(Chat_range[1])):
            GET_Session_Chat +=1
            app.loop.create_task(POST_SESSION('CHAT', destNum))
        elif (dest_num_int >= int(FT_range[0]) and dest_num_int <= int(FT_range[1])):
            GET_Session_FT += 1
            app.loop.create_task(POST_SESSION('FT', destNum))
        elif (dest_num_int >= int(PM_range[0]) and dest_num_int <= int(PM_range[1])):
            GET_Session_PM += 1
            app.loop.create_task(POST_SESSION('PM', destNum))
        elif (dest_num_int >= int(LM_range[0]) and dest_num_int <= int(LM_range[1])):
            GET_Session_LM += 1
            app.loop.create_task(POST_SESSION('LM', destNum))
        elif (dest_num_int >= int(HTTP_FT_range[0]) and dest_num_int <= int(HTTP_FT_range[1])):
            GET_Session_HTTPFT += 1
            app.loop.create_task(POST_SESSION('HTTPFT', destNum))
    else:
        print("Dest_Num not found in GET_Session packet.")
    return web.Response()

async def handle_get_msrp(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global GET_MSRP_Chat, GET_MSRP_FT, GET_MSRP_LM, GET_MSRP_HTTPFT
    req_url = str(request.url)
    origNum = findall(r'origUserId=\+1(\d{10})', req_url)[0]
    destNum = findall(r'destUserId=\+1(\d{10})', req_url)[0]
    dest_num_int = int(destNum)
    if (dest_num_int >= int(Chat_range[0]) and dest_num_int <= int(Chat_range[1])):
        GET_MSRP_Chat += 1
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
        tp_data_last = '","CreateTime":"","GenericHeaders":"","sessionId":-1}}'
        data_to_send_in_200OK = '{"rsp":{"Messages":['
        for i in range(NUM_OF_MSRP_EXPECTED_IN_SESSION_CHAT):
            Content_X = Content_Initial_part_1 + "imdn" + str(i + 1) + Content_data_last_part
            tp_data_X = convert_to_base64(tp_data_initial + str(convert_to_base64(Content_X).decode()) + tp_data_last)
            message_X = '{"origUserId":"+1' + origNum + '","destUserId":"+1' + destNum + '","messageId":"' \
                        + str(randint(0000, 9999)) + str(randint(0000, 9999)) + '-5cba-149d-bb2c-35' \
                        + origNum + '","tpDataType":"base64","tpData":"' + str(tp_data_X.decode()) + '"}'
            data_to_send_in_200OK += message_X + ','
        data_to_send_in_200OK = data_to_send_in_200OK[:-1]
        data_to_send_in_200OK += '],"subType":"On"}}'
    elif (dest_num_int >= int(FT_range[0]) and dest_num_int <= int(FT_range[1])):
        GET_MSRP_FT += 1
        data_to_send_in_200OK = FILE_DATA_BASE64
    elif (dest_num_int >= int(LM_range[0]) and dest_num_int <= int(LM_range[1])):
        GET_MSRP_LM += 1
        data_to_send_in_200OK = LM_DATA_BASE64
    elif (dest_num_int >= int(HTTP_FT_range[0]) and dest_num_int <= int(HTTP_FT_range[1])):
        GET_MSRP_HTTPFT += 1
        Content_Initial_part_1 = 'From: ' + origNum + '<sip:+1' + origNum + '@rcse-dls-capacity.mavenir.lab>\r\n' \
                                                                            'NS: imdn<urn:ietf:params:imdn>\r\n' \
                                                                            'imdn.Message-ID: mstore_imdn' + origNum + '-' + destNum
        Content_Initial_part_2 = '\r\nimdn.Disposition-Notification: positive-delivery, display\r\n' \
                                 'DateTime: 2018-02-28T15:17:33Z\r\n' \
                                 'To: <sip:+1' + destNum + '@rcse-dls-capacity.mavenir.lab>\r\n' \
                                                           '\r\n' \
                                                           'Content-type: application/vnd.gsma.rcs-ft-http+xml;charset=utf-8\r\n ' \
                                                           'Content-length: 679\r\n\r\n'
        Content_Data = '<?xml version="1.0" encoding="UTF-8"?><file xmlns="urn:gsma:params:xml:ns:rcs:rcs:fthttp"><file-info type="thumbnail"><file-size>5132</file-size><content-type>image/jpeg</content-type><data url="http://172.24.3.230:9999/mStoreRoot/thumbnail/39393DF5B7ACE9D1A312444FF6FDA0A6E1C1DC6E1FBF1FC5F49C719050ECC2BA" until="2017-08-15T14:48:49.000Z"/></file-info><file-info type="file"><file-size>3132</file-size><file-name>img_20141020_183610_small_1413810372748.jpg</file-name><content-type>image/jpeg</content-type><data url="http://172.24.3.230:9999/mStoreRoot/file/39393DF5B7ACE9D1A312444FF6FDA0A6E1C1DC6E1FBF1FC5F49C719050ECC2BA" until="2017-08-15T14:48:48.000Z"/></file-info></file>'
        Content_data_last_part = Content_Initial_part_2 + Content_Data
        tp_data_initial = '{"req":{"SuccessReport":1,"FailureReport":1,"ContentDisposition":""' \
                          ',"ImdnRequested":1,"Content-Type":"message/cpim","Content":"'
        tp_data_last = '","CreateTime":"","GenericHeaders":"","sessionId":-1}}'
        data_to_send_in_200OK = '{"rsp":{"Messages":['
        for i in range(1):
            Content_X = Content_Initial_part_1 + "imdn" + str(i + 1) + Content_data_last_part
            tp_data_X = convert_to_base64(tp_data_initial + str(convert_to_base64(Content_X).decode()) + tp_data_last)
            message_X = '{"origUserId":"+1' + origNum + '","destUserId":"+1' + destNum + '","messageId":"' \
                        + str(randint(0000, 9999)) + str(randint(0000, 9999)) + '-5cba-149d-bb2c-35' \
                        + origNum + '","tpDataType":"base64","tpData":"' + str(tp_data_X.decode()) + '"}'
            data_to_send_in_200OK += message_X + ','
        data_to_send_in_200OK = data_to_send_in_200OK[:-1]
        data_to_send_in_200OK += '],"subType":"On"}}'
    return web.Response(body=data_to_send_in_200OK, content_type='application/json')

async def handle_delete_data(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global DELETE_MSRP_Chat, DELETE_PM
    http_header = str(request.url)
    http_body = await request.read()
    message_id_list = findall(b'\{"messageId":"(.*?)"\}', http_body)
    message_list = ''
    for i in message_id_list:
        ok_status = '{"messageId":"' + str(i.decode()) + '","status":"200"}'
        message_list += ok_status + ','
    message_list = message_list[:-1]
    http_resp_data = '{"rsp":{"ResponseList":[' + message_list + ']}}'
    if "msrpImData" in http_header:
        DELETE_MSRP_Chat += 1
    elif "pageMode" in http_header:
        DELETE_PM += 1
    return web.Response(body=http_resp_data, content_type='application/json')

async def handle_delete_session(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global DELETE_Session_Chat, DELETE_FT, DELETE_LM
    http_header = str(request.url)
    if "imSessInfo" in http_header:
        DELETE_Session_Chat += 1
    elif "ftSessInfo" in http_header:
        DELETE_FT += 1
    elif "lmSessInfo" in http_header:
        DELETE_LM += 1
    return web.Response(status=204)

async def handle_slash(request):
    global display_task_started
    if not display_task_started:
        app.loop.create_task(display_count())
        display_task_started = True
    global POST_SLASH
    message_list = ''
    http_body = await request.read()
    message_id_list = findall(b'\{"messageId":"(.*?)","', http_body)
    for i in message_id_list:
        ok_status = '{"messageId":"' + str(i.decode()) + '","status":"204"}'
        message_list += ok_status + ','
    message_list = message_list[:-1]
    http_resp_data = '{"rsp":{"ResponseList":[' + message_list + ']}}'
    POST_SLASH += 1
    return web.Response(body=http_resp_data, content_type='application/json')


async def display_count():
    print("Display coroutine started")
    while True:
        await sleep(5)
        print("################################################################")
        print("RECV_STORE_POST_Session")
        print("   Chat_session:  " + str(POST_Store_Chat_Session) +
              "  FT_session:  " + str(POST_Store_FT_Session) +
              "  PM_session: " + str(POST_Store_PM) +
              "  LM_session: " + str(POST_Store_LM_Session) +
              "  GC_session: " + str(POST_Store_GC_Session))
        print("RECV_STORE_POST_Data")
        print("   Chat_MSRP: " + str(POST_Store_Chat_MSRP) +
              "  FT_MSRP: " + str(POST_Store_FT_MSRP) +
              "  LM_MSRP: " + str(POST_Store_LM_MSRP))
        print("RECV_GET_Session")
        print("   Chat_session: " + str(GET_Session_Chat) +
              "  FT_session: " + str(GET_Session_FT) +
              "  PM_session: " + str(GET_Session_PM) +
              "  LM_session: " + str(GET_Session_LM) +
              "  No_RESP_Needed: " + str(GET_Session_NoRespNeeded))
        print("SEND_POST_Session")
        print("   Chat_session: " + str(POST_Session_Chat) +
              "  FT_session: " + str(POST_Session_FT) +
              "  PM_session: " + str(POST_Session_PM) +
              "  LM_session: " + str(POST_Session_LM))
        print("RECV_GET_MSRP_Data")
        print("   Chat_MSRP: " + str(GET_MSRP_Chat) +
              "  FT_MSRP: " + str(GET_MSRP_FT) +
              "  LM_MSRP: " + str(GET_MSRP_LM))
        print("DELETE_DATA")
        print("   Chat_session: " + str(DELETE_Session_Chat) +
              "  Chat_Data: " + str(DELETE_MSRP_Chat) +
              "  FT_session: " + str(DELETE_FT) +
              "  PM: " + str(DELETE_PM) +
              "  LM_session: " + str(DELETE_LM))
        print("RECV_POST_UPDATE_PACKET")
        print("   UPDATE: " + str(POST_Store_Update))
        print("ERROR_403_PACKET")
        print("   ERROR_403: " + str(POST_SLASH))

app = web.Application()
app.add_routes([web.post('/mStoreRoot/V1/SF/store/{info}', handle_post_store),
                web.get('/mStoreRoot/V1/SF/forward/{info}', handle_get_session),
                web.get('/mStoreRoot/V1/SF/retrieve/{info}', handle_get_msrp),
                web.post('/mStoreRoot/V1/SF/delete/{info}', handle_delete_data),
                web.delete('/mStoreRoot/V1/SF/delete/{info}', handle_delete_session),
                web.post('/', handle_slash)])
web.run_app(app, host=LOCAL_HOST, port=LOCAL_PORT)


