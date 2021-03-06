from re import findall
from random import randint
import asyncio


file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()
app_serv_port_start = []
log_file_obj = open("mt_stats.txt", 'w')
log_file_obj.write("Success,Failed\n")
log_file_obj.flush()


LOCAL_HOST = file_lines[0].split('=')[1].strip()
TCP_PORT = int(file_lines[2].split('=')[1].strip())
RMS_HOST = file_lines[3].split('=')[1].strip()
msrp_message_to_be_received = int(file_lines[4].split('=')[1].strip())
task_timeout = int(file_lines[5].split('=')[1].strip())
delay_between_successive_messages = float(file_lines[6].split('=')[1].strip())
fqdn = file_lines[7].split('=')[1].strip()
app_serv_port_start_from_file = file_lines[8].split('=')[1].strip().rstrip(']').lstrip('[').split(',')
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
    global dict_call_num
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
    data_full = ''
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
    except asyncio.CancelledError as e:
        #print("Timeout exception during read")
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

async def is_comp_recv(reader, writer, fromTag, toTag):
    return True

async def msrp_data_recv(reader, writer, fromTag, toTag, fromNum, toNum):
    search_str = "Content-type: application/vnd.gsma.rcs-ft-http+xml;charset=utf-8"
    try:
        result = await read_search(reader, search_str.encode(), search_str, True, True)
    except asyncio.CancelledError as e:
        return False
    if result[0] and result[1] and result[2]:
        data_to_send = 'MSRP ' + result[1] + ' 200 OK\r\nTo-Path: ' + toTag + '\r\nFrom-Path: ' + fromTag + '\r\n-------' + result[1] + '$\r\n'
        data_to_send_encoded = data_to_send.encode()
        writer.write(data_to_send_encoded)
        try:
            await writer.drain()
        except ConnectionError as e:
            return False
    else:
        #print("MSRP data recv failed")
        return False
    await asyncio.sleep(delay_between_successive_messages)
    msrp_xml = '<?xml version="1.0" encoding="utf-8"?><imdn xmlns="urn:ietf:params:xml:ns:imdn"><message-id> ' \
               + result[2] + \
               '</message-id><datetime>2012-06-07T17:40:31</datetime><delivery-notification><status><delivered/></status></delivery-notification></imdn>'
    len_msrp_xml = len(msrp_xml)
    msrp_data = "From: <sip:" + str(fromNum) + "@" + fqdn + ">\r\n" \
                "To: <sip:" + str(toNum) + "@" + fqdn + ">\r\n" \
                "NS: imdn <urn:ietf:params:imdn>\r\n" \
                "imdn.Message-ID: " + \
                result[2] + "\r\n\r\n" \
                "Content-type: message/imdn+xml\r\n" \
                "Content-Disposition: notification\r\n" \
                "Content-length: " + str(len_msrp_xml + 2) + "\r\n\r\n" \
                + msrp_xml + "\r\n"
    message_ID = "term" + str(randint(100000, 999999))
    transId = message_ID
    byte_range = "1-" + str(len(msrp_data)) + "/" + str(len(msrp_data))
    full_msrp_message = "MSRP " + transId + " SEND\r\n" \
                        "To-Path: " + toTag + "\r\n" \
                        "From-Path: " + fromTag + "\r\n" \
                        "Message-ID: messId" + message_ID + "\r\n" \
                        "Byte-Range: " + byte_range + "\r\n" \
                        "Content-Type: message/cpim\r\n\r\n" \
                        + msrp_data + "\r\n-------" + transId + "$\r\n"
    full_msrp_message_encoded = full_msrp_message.encode()
    writer.write(full_msrp_message_encoded)
    try:
        await writer.drain()
    except ConnectionError as e:
        return False
    await asyncio.sleep(delay_between_successive_messages)
    msrp_xml = '<?xml version="1.0" encoding="utf-8"?><imdn xmlns="urn:ietf:params:xml:ns:imdn"><message-id> ' \
               + result[2] + \
               '</message-id><datetime>2012-06-07T17:40:31</datetime><display-notification><status><displayed/></status></display-notification></imdn>'
    len_msrp_xml = len(msrp_xml)
    msrp_data = "From: <sip:" + str(fromNum) + "@" + fqdn + ">\r\n" \
                "To: <sip:" + str(toNum) + "@" + fqdn + ">\r\n" \
                "NS: imdn <urn:ietf:params:imdn>\r\n" \
                "imdn.Message-ID: " + \
                result[2] + "\r\n\r\n" \
                "Content-type: message/imdn+xml\r\n" \
                "Content-Disposition: notification\r\n" \
                "Content-length: " + str(len_msrp_xml + 2) + "\r\n\r\n" \
                + msrp_xml + "\r\n"
    message_ID = "term" + str(randint(100000, 999999))
    transId = message_ID
    byte_range = "1-" + str(len(msrp_data)) + "/" + str(len(msrp_data))
    full_msrp_message = "MSRP " + transId + " SEND\r\n" \
                        "To-Path: " + toTag + "\r\n" \
                        "From-Path: " + fromTag + "\r\n" \
                        "Message-ID: messId" + message_ID + "\r\n" \
                        "Byte-Range: " + byte_range + "\r\n" \
                        "Content-Type: message/cpim\r\n\r\n" \
                        + msrp_data + "\r\n-------" + transId + "$\r\n"
    full_msrp_message_encoded = full_msrp_message.encode()
    writer.write(full_msrp_message_encoded)
    try:
        await writer.drain()
        return True
    except ConnectionError as e:
        return False

async def msrp_handler(fromTag, toTag, toPort, from_num, to_num, callNum):
    recv_total = 0
    global success_call_count
    global fail_call_count
    global dict_connection
    global dict_call_num
    try:
        reader, writer = await connect(toPort, fromTag, toTag)
        if reader and writer:
            dict_call_num[callNum][2] = writer
            for i in range(msrp_message_to_be_received):
                result = await is_comp_recv(reader, writer, fromTag, toTag)
                if result :
                    result = await is_comp_recv(reader, writer, fromTag, toTag)
                    if result :
                        result = await msrp_data_recv(reader, writer, fromTag, toTag, from_num, to_num)
                        if result :
                            recv_total += 1
                        else:
                            break
                    else:
                        break
                else:
                    break
            if recv_total == msrp_message_to_be_received:
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
        #print("Exception in main loop")
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
            TCP_fromID = findall(r'From-Path:msrp://(.*):(.*?)/(.*?);tcp', TCP_data)
            TCP_toID = findall(r'a=path:msrp://(.*):(.*?)/(.*?);tcp', TCP_data)
            from_num_list = findall(r'a=FROMNUM:(.*?)FROMNUM', TCP_data)
            to_num_list = findall(r'a=TONUM:(.*?)TONUM', TCP_data)
            if TCP_fromID and TCP_toID and from_num_list and to_num_list:
                fromTag = 'msrp://' + TCP_fromID[0][0] + ':' + TCP_fromID[0][1] + '/' + TCP_fromID[0][2] + ';tcp'
                toTag = 'msrp://' + TCP_toID[0][0] + ':' + TCP_toID[0][1] + '/' + TCP_toID[0][2] + ';tcp'
                toPort = TCP_toID[0][1]
                try:
                    call_num += 1
                    task_id = loop.create_task(msrp_handler(fromTag, toTag, toPort, from_num_list[0], to_num_list[0], call_num))
                    dict_call_num[call_num] = [task_id,'InProgress','']
                    loop.create_task(task_canceller(call_num))
                except (asyncio.CancelledError, ConnectionError, asyncio.TimeoutError) as e:
                    print("Exception in main loop: " + str(e))

dict_connection = {}
dict_call_num = {}
success_call_count = 0
fail_call_count = 0
call_num = 0
MSRP_end_char = b'$\r\n'

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
