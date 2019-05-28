from re import findall
from random import randint
import asyncio

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()
app_serv_port_start = []
log_file_obj = open("mo_stats.txt", 'w')
log_file_obj.write("Success,Failed\n")
log_file_obj.flush()

LOCAL_HOST = file_lines[0].split('=')[1].strip()
TCP_PORT = int(file_lines[1].split('=')[1].strip())
RMS_HOST = file_lines[3].split('=')[1].strip()
msrp_message_to_be_sent = int(file_lines[4].split('=')[1].strip())
task_timeout = int(file_lines[5].split('=')[1].strip())
delay_between_successive_messages = float(file_lines[6].split('=')[1].strip())
fqdn = file_lines[7].split('=')[1].strip()
app_serv_port_start_from_file = file_lines[8].split('=')[1].strip().rstrip(']').lstrip('[').split(',')
for p in range(len(app_serv_port_start_from_file)):
    app_serv_port_start.append(int(app_serv_port_start_from_file[p]))
app_serv_port_range = int(file_lines[9].split('=')[1].strip())
mstore_ip =file_lines[10].split('=')[1].strip()
mstore_port = int(file_lines[11].split('=')[1].strip())

for p in range(len(app_serv_port_start_from_file)):
    app_serv_port_start.append(int(app_serv_port_start_from_file[p]))
app_serv_port_range = int(file_lines[9].split('=')[1].strip())

async def counter_display():
    while True:
        await asyncio.sleep(5)
        print(success_call_count, fail_call_count)
        log_file_obj.write(str(success_call_count) + ',' + str(fail_call_count)+ "\n")
        log_file_obj.flush()

async def task_canceller(callNum):
    await asyncio.sleep(task_timeout)
    task_Id_for_cancelling = dict_call_num[callNum][0]
    status = dict_call_num[callNum][1]
    if status == "InProgress":
        task_Id_for_cancelling.cancel()
    writer = dict_call_num[callNum][2]
    if writer:
        writer.close()
    del dict_call_num[callNum]
    return

async def read_search(reader, end_delimiter, search_string, transid_needed, imdnid_needed):
    result = [False, '', '']
    try:
        while True:
            data_read = await reader.readuntil(end_delimiter)
            data_full = data_read.decode()
            if search_string in data_full:
                result[0] = True
                if transid_needed:
                    transId = findall(r'MSRP (.*?) SEND', data_full)
                    result[1] = transId[0]
                if imdnid_needed:
                    imdnId = findall(r'imdn.Message-ID: (.*?)\r\n', data_full)
                    result[2] = imdnId[0]
                return result
            else:
                continue
    except asyncio.TimeoutError as e:
        #print("Exception timeout in read search")
        return [False, '', '']

async def send_empty(reader, writer, fromTag, toTag):
    byte_range = "1-0/0"
    message_ID = "empty"
    trans_ID = message_ID
    full_empty_message = "MSRP " + trans_ID + " SEND\r\n" \
                                "To-Path: " + toTag + "\r\n" \
                                "From-Path: " + fromTag + "\r\n" \
                                "Message-ID: " + message_ID + "\r\n" \
                                "Byte-Range: " + byte_range + "\r\n" \
                                "Success-Report: no\r\n" \
                                "Failure-Report: yes\r\n" \
                                + "-------" + trans_ID + "$\r\n"
    full_empty_message_encoded = full_empty_message.encode()
    writer.write(full_empty_message_encoded)
    try:
        await writer.drain()
    except ConnectionError as e:
        return False
    search_str = "empty 200"
    try:
        result = await read_search(reader, MSRP_end_char, search_str, False, False)
    except asyncio.CancelledError as e:
        return False
    if result[0]:
        return True
    else:
        return False

async def connect(remote_port, fromTag, toTag):
    if (len(dict_connection[remote_port]) > 0):
        reader, writer = dict_connection[remote_port].pop(0)
        empty_sent = await send_empty(reader, writer, fromTag, toTag)
        if empty_sent:
            return [reader, writer]
    try:
        reader, writer = await asyncio.open_connection(host=RMS_HOST, port=remote_port)
        empty_sent = await send_empty(reader, writer, fromTag, toTag)
        if empty_sent:
            return [reader, writer]
    except Exception as e:
        print("Exception in connect")
        return ['', '']


async def is_composing_send(reader, writer, fromTag, toTag, toPort):
    return True

async def send_msrpdata_recv_imdn(reader, writer, fromTag, toTag, from_num, to_num, imdn_count):
    msrp_data_fixed = "\r\n" \
                      "From: <sip:" + str(from_num) + "@" + fqdn + ">\r\n" \
                      "To: <sip:" + str(to_num) + "@" + fqdn + ">\r\n" \
                      "DateTime: 2012-06-07T17:40:29\r\n" \
                      "Content-type: application/vnd.gsma.rcs-ft-http+xml;charset=utf-8\r\n" \
                      "Content-length: " + str(msrp_data_length) + "\r\n" \
                      "NS: imdn <urn:ietf:params:imdn>\r\n" \
                      "imdn.Disposition-Notification: positive-delivery, display\r\n"
    msrp_data = msrp_data_fixed + \
                'imdn.Message-ID: imdn' + str(randint(10000, 99999)) + '\r\n' \
                '\r\n' + msrp_data_part
    byte_range = "1-" + str(len(msrp_data)) + "/" + str(len(msrp_data))
    message_ID = "mav" + str(randint(100000, 999999))
    trans_ID = message_ID
    full_msrp_message = "MSRP " + trans_ID + " SEND\r\n" \
                        "To-Path: " + toTag + "\r\n" \
                        "From-Path: " + fromTag + "\r\n" \
                        "Message-ID: messId" + message_ID + "\r\n" \
                        "Success-Report: no\r\n" \
                        "Failure-Report: yes\r\n" \
                        "Byte-Range: " + byte_range + "\r\n" \
                        "Content-Type: message/cpim\r\n" \
                        + msrp_data + "\r\n\r\n-------" + trans_ID + "$\r\n"
    full_msrp_message_encoded = full_msrp_message.encode()
    writer.write(full_msrp_message_encoded)
    try:
        await writer.drain()
    except ConnectionError as e:
        return False
    imdn_recvd = 0
    for i in range(imdn_count):
        search_str = "Content-Disposition: notification"
        try:
            result = await read_search(reader, search_str.encode(), search_str, True, False)
        except asyncio.CancelledError as e:
            return False
        if result[0] and result[1]:
            data_to_send = 'MSRP ' + result[1] + ' 200 OK\r\nTo-Path: ' + toTag + '\r\nFrom-Path: ' + fromTag + '\r\n-------' + result[1] + '$\r\n'
            data_to_send_encoded = data_to_send.encode()
            writer.write(data_to_send_encoded)
            try:
                await writer.drain()
            except ConnectionError as e:
                return False
            imdn_recvd += 1
            if imdn_recvd == imdn_count:
                return True
            else:
                continue
        else:
            return False

async def msrp_handler(fromTag, toTag, toPort, from_num, to_num, term_party_count, callNum):
    sent_total = 0
    global success_call_count
    global fail_call_count
    global dict_connection
    global dict_call_num
    imdn_count = 2*int(term_party_count)
    try:
        reader, writer = await connect(toPort, fromTag, toTag)
        if reader and writer:
            dict_call_num[callNum][2] = writer
            for i in range(msrp_message_to_be_sent):
                await asyncio.sleep(delay_between_successive_messages)
                result = await is_composing_send(reader, writer, fromTag, toTag, toPort)
                if result :
                    await asyncio.sleep(delay_between_successive_messages)
                    result = await is_composing_send(reader, writer, fromTag, toTag, toPort)
                    if result :
                        await asyncio.sleep(delay_between_successive_messages)
                        result = await send_msrpdata_recv_imdn(reader, writer, fromTag, toTag, from_num, to_num, imdn_count)
                        if result :
                            sent_total += 1
                        else:
                            break
                    else:
                        break
                else:
                    break
            if sent_total == msrp_message_to_be_sent:
                success_call_count += 1
                dict_call_num[callNum][1] = "Completed"
                #dict_connection[toPort].append((reader, writer))
            else:
                #print("failed call")
                fail_call_count += 1
                writer.close()
        else:
            fail_call_count += 1
            #print("no reader and writer found")
    except Exception as e:
        # print("Exception in main loop")
        fail_call_count += 1
        writer.close()
    finally:
        return

class TCPServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, TCP_data_raw):
        global call_num
        global dict_call_num
        TCP_split = str(TCP_data_raw.decode()).split("\r\n\r\n")
        for TCP_data in TCP_split:
            TCP_fromID = findall(r'From-Path:msrp://(\[.*\]):(.*?)/(.*?);tcp', TCP_data)
            TCP_toID = findall(r'a=path:msrp://(\[.*\]):(.*?)/(.*?);tcp', TCP_data)
            from_num_list = findall(r'a=FROMNUM:(.*?)FROMNUM', TCP_data)
            to_num_list = findall(r'a=TONUM:(.*?)TONUM', TCP_data)
            term_party_count = findall(r'term=COUNT(.*?)COUNT', TCP_data)
            if TCP_fromID and TCP_toID and from_num_list and to_num_list and term_party_count:
                fromTag = 'msrp://' + TCP_fromID[0][0] + ':' + TCP_fromID[0][1] + '/' + TCP_fromID[0][2] + ';tcp'
                toTag = 'msrp://' + TCP_toID[0][0] + ':' + TCP_toID[0][1] + '/' + TCP_toID[0][2] + ';tcp'
                toPort = TCP_toID[0][1]
                try:
                    call_num += 1
                    task_id = loop.create_task(msrp_handler(fromTag, toTag, toPort, from_num_list[0], to_num_list[0], term_party_count[0],call_num))
                    dict_call_num[call_num] = [task_id,'InProgress','']
                    loop.create_task(task_canceller(call_num))
                except (asyncio.CancelledError, ConnectionError) as e:
                    print("exception in main loop")

dict_connection = {}
dict_call_num = {}
success_call_count = 0
fail_call_count = 0
call_num = 0
msrp_data_part = '<?xml version="1.0" encoding="UTF-8"?><file xmlns="urn:gsma:params:xml:ns:rcs:rcs:fthttp"><file-info type="thumbnail"><file-size>5132</file-size><content-type>image/jpeg</content-type><data url="http://[' + str(mstore_ip) + ']:' + str(mstore_port) + '/mStoreRoot/thumbnail/39393DF5B7ACE9D1A312444FF6FDA0A6E1C1DC6E1FBF1FC5F49C719050ECC2BA" until="2017-08-15T14:48:49.000Z"/></file-info><file-info type="file"><file-size>3132</file-size><file-name>img_20141020_183610_small_1413810372748.jpg</file-name><content-type>image/jpeg</content-type><data url="http://[' + str(mstore_ip) + ']:' + str(mstore_port) + '/mStoreRoot/file/39393DF5B7ACE9D1A312444FF6FDA0A6E1C1DC6E1FBF1FC5F49C719050ECC2BA" until="2017-08-15T14:48:48.000Z"/></file-info></file>'
msrp_data_length = len(msrp_data_part)
MSRP_end_char = b'$\r\n'

is_composing_data = '\r\n' \
                    '\r\n' \
                    '<?xml version="1.0" encoding="UTF-8"?>\r\n' \
                    '<isComposing xmlns="urn:ietf:params:xml:ns:im-iscomposing"\r\n' \
                    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\r\n' \
                    'xsi:schemaLocation="urn:ietf:params:xml:ns:im-composing iscomposing.xsd">\r\n' \
                    '<state>active</state>\r\n' \
                    '<contenttype>text/plain</contenttype>\r\n' \
                    '<lastactive>2015-10-28T05:14:29.000Z</lastactive>\r\n' \
                    '<refresh>60</refresh>\r\n' \
                    '</isComposing>'
len_is_composing_data = str(len(is_composing_data))

for i in app_serv_port_start:
    for j in range(app_serv_port_range):
        dict_connection[str(i + j)] = []

try:
    loop = asyncio.get_event_loop()
    coro = loop.create_server(TCPServer, LOCAL_HOST, TCP_PORT)
    server = loop.run_until_complete(coro)
    print("Listening on TCP port: " + str(TCP_PORT))
    loop.create_task(counter_display())
    loop.run_forever()
except Exception as e:
    pass
finally:
    file_obj.close()
    log_file_obj.close()
