import asyncio
from re import findall
from random import randint

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()
app_serv_port_start = []

LOCAL_HOST = file_lines[0].split('=')[1].strip()
UDP_PORT = int(file_lines[1].split('=')[1].strip())
RMS_HOST = file_lines[4].split('=')[1].strip()
task_timeout = int(file_lines[5].split('=')[1].strip())
fqdn = file_lines[6].split('=')[1].strip()
app_serv_port_start_from_file = file_lines[7].split('=')[1].strip().rstrip(']').lstrip('[').split(',')
for p in range(len(app_serv_port_start_from_file)):
    app_serv_port_start.append(int(app_serv_port_start_from_file[p]))
app_serv_port_range = int(file_lines[8].split('=')[1].strip())
image_file = file_lines[9].split('=')[1].strip()
CHUNK_SIZE = int(file_lines[10].split('=')[1].strip())

async def counter_display():
    while True:
        await asyncio.sleep(5)
        print("Success: " + str(success_call_count) + "   Failed: " + str(fail_call_count))

async def task_canceller(callNum):
    await asyncio.sleep(task_timeout)
    if dict_call_num[callNum][1] == "InProgress":
        dict_call_num[callNum][0].cancel()
    del dict_call_num[callNum]
    return

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
    except asyncio.CancelledError as e:
        return False
    data_read = b''
    while True:
        try:
            temp = await reader.read(102400)
            data_read += temp
            if not (b'200 OK' in data_read):
                continue
            else:
                return True
        except asyncio.CancelledError as e:
            print("no 200OK for empty")
            return False
        except asyncio.LimitOverrunError as e:
            print("no 200OK for empty")
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

async def send_msrp_data(reader, writer, fromTag, toTag, from_num, to_num):
    sent_packet_count = 0
    Initial_data_1 = "From: <sip:" + str(from_num) + "@" + fqdn + ">\r\n" \
                     "DateTime: 2015-05-12T13:20:56+00:00\r\n" \
                     "NS: MD <mailto:RCS@t-mobile.com>\r\n" \
                      "MD.Direction: In\r\n" \
                      "To: <sip:" + str(to_num) + "@" + fqdn + ">\r\n\r\n" \
                      "Content-Type: image/*\r\nContent-length: " + str(DATA_SIZE) + "\r\n\r\n"
    len_initial_text = len(Initial_data_1)
    total_len = DATA_SIZE + len_initial_text
    num_of_chunks_to_send, remainder = divmod(total_len, CHUNK_SIZE)
    if (remainder != 0):
        num_of_chunks_to_send += 1
    Full_user_data = Initial_data_1.encode() + msrp_data_part
    Byte_range_start = 0
    random_num = randint(100000, 900000)
    Message_ID = "mav" + str(random_num)
    while (sent_packet_count < num_of_chunks_to_send):
        random_num = randint(100000, 900000)
        Session_ID = "mav" + str(random_num)
        if(sent_packet_count == num_of_chunks_to_send-1):
            Byte_range_end = total_len
            end_char = '$\r\n'
        else:
            Byte_range_end = (sent_packet_count+1) * CHUNK_SIZE
            end_char = '+\r\n'
        Byte_range = str(Byte_range_start + 1) + "-" + str(Byte_range_end)
        Data = Full_user_data[Byte_range_start : Byte_range_end] +("\r\n-------" + Session_ID + end_char).encode()
        msrp_packet_to_send = ("MSRP " + Session_ID + " SEND\r\nTo-Path: " + toTag + "\r\nFrom-Path: " +\
                              fromTag + "\r\nMessage-ID: " + Message_ID + "\r\nSuccess-Report: " \
                                "no\r\nFailure-Report: yes\r\nByte-Range: " + Byte_range + "/" + str(total_len) \
                               + "\r\nContent-Type: message/cpim\r\n\r\n").encode() + Data
        writer.write(msrp_packet_to_send)
        try:
            await writer.drain()
        except ConnectionError as e:
            print("connection error while sending")
            return False
        except asyncio.CancelledError as e:
            return False
        try:
            result_read = await reader.readuntil(MSRP_end_char)
            result_read = result_read.decode()
            if ("200 OK" in result_read):
                sent_packet_count += 1
                Byte_range_start = Byte_range_end
                continue
        except asyncio.CancelledError as e:
            return False
    return True

async def msrp_handler(fromTag, toTag, toPort, from_num, to_num, callNum):
    global success_call_count
    global fail_call_count
    global dict_connection
    global dict_call_num
    try:
        reader, writer = await connect(toPort, fromTag, toTag)
        if reader and writer:
            result = await send_msrp_data(reader, writer, fromTag, toTag, from_num, to_num)
            if result :
                success_call_count += 1
                dict_call_num[callNum][1] = "Completed"
                dict_connection[toPort].append((reader, writer))
            else:
                fail_call_count += 1
                writer.close()
        else:
            fail_call_count += 1
    except Exception as e:
        fail_call_count += 1
        writer.close()
    finally:
        return

class UDPServer:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, UDP_data, addr):
        global call_num
        global dict_call_num
        UDP_data = str(UDP_data.decode())
        UDP_fromID = findall(r'From-Path:msrp://(.*):(.*?)/(.*?);tcp', UDP_data)
        UDP_toID = findall(r'a=path:msrp://(.*):(.*?)/(.*?);tcp', UDP_data)
        from_num_list = findall(r'a=FROMNUM:(.*?)FROMNUM', UDP_data)
        to_num_list = findall(r'a=TONUM:(.*?)TONUM', UDP_data)
        if UDP_fromID and UDP_toID and from_num_list and to_num_list :
            fromTag = 'msrp://' + UDP_fromID[0][0] + ':' + UDP_fromID[0][1] + '/' + UDP_fromID[0][2] + ';tcp'
            toTag = 'msrp://' + UDP_toID[0][0] + ':' + UDP_toID[0][1] + '/' + UDP_toID[0][2] + ';tcp'
            toPort = UDP_toID[0][1]
            try:
                call_num += 1
                task_id = loop.create_task(msrp_handler(fromTag, toTag, toPort, from_num_list[0], to_num_list[0], call_num))
                dict_call_num[call_num] = [task_id,'InProgress']
                loop.create_task(task_canceller(call_num))
            except (asyncio.CancelledError, ConnectionError) as e:
                print("exception in main loop")

dict_connection = {}
dict_call_num = {}
success_call_count = 0
fail_call_count = 0
call_num = 0


msrp_data_part = open(image_file, 'rb').read();
DATA_SIZE = len(msrp_data_part)
MSRP_end_char = b'$\r\n'

for i in app_serv_port_start:
    for j in range(app_serv_port_range):
        dict_connection[str(i + j)] = []

loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(UDPServer, local_addr=(LOCAL_HOST, UDP_PORT))
transport, protocol = loop.run_until_complete(listen)
print("Listening on UDP port: " + str(UDP_PORT))
loop.create_task(counter_display())
loop.run_forever()

