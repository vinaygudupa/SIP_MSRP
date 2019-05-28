import asyncio, binascii, ipaddress

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()
line_count = len(file_lines)
number_range_list = []
user_data_dict = {}
user_data_count = 0
count_dict = {}

LOCAL_HOST = file_lines[0].split('=')[1].strip()
PORT = int(file_lines[1].split('=')[1].strip())
timeout = int(file_lines[2].split('=')[1].strip())

for i in range(len(file_lines)):
    if file_lines[i].startswith('user_set_'):
        user_data_name = file_lines[i].split('=')[0].strip()
        user_data = file_lines[i].split('=')[1].strip()
        user_data_dict[user_data_name] = user_data.encode()

    if file_lines[i].startswith('range_'):
        data = file_lines[i].split('=')[1]
        number = int(data.split(":")[0].strip())
        num_range = int(data.split(":")[1].strip())
        user_data = data.split(":")[2].strip()
        number_range_list.append([number,number+num_range-1,user_data])

for i in number_range_list:
    udata_name = i[2]
    i[2] = (udata_name, user_data_dict[udata_name])
    count_dict[udata_name] = 0
count_dict['user_set_default'] = 0

udr_vendor_specfic_app_id = b'\x00\x00\x01\x04\x40\x00\x00\x20\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x01\x02\x40\x00\x00\x0c\x01\x00\x00\x01'
udr_auth_session_state = b'\x00\x00\x01\x15\x40\x00\x00\x0c\x00\x00\x00\x01'
udr_result_code = b'\x00\x00\x01\x0c\x40\x00\x00\x0c\x00\x00\x07\xd1'
udr_origin_host = b'\x00\x00\x01\x08\x40\x00\x00\x17\x73\x70\x73\x2e\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62\x00'
udr_origin_realm = b'\x00\x00\x01\x28\x40\x00\x00\x13\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62\x00'
udata_1 = b'\x00\x00\x02\xbe\xc0\x00'
udata_2 = b'\x00\x00\x28\xaf' + b'<?xml version="1.0" encoding="UTF-8"?><Sh-Data><PublicIdentifiers><MSISDN>'
udata_3 = b'</MSISDN></PublicIdentifiers><RepositoryData><ServiceIndication>RCS_SUBPROFILE</ServiceIndication><SequenceNumber>0</SequenceNumber><ServiceData><Subscriber version="1.0"><SubStatus>ACT</SubStatus><IMSI>1234'
udata_4 = b'</IMSI><SubType>POSTPAID</SubType><MSISDN>'
udata_5 = b'</MSISDN>'
udata_6 = b'<OperatorId>TMO</OperatorId><Language>En</Language>'
udata_7 = b'</Subscriber></ServiceData></RepositoryData></Sh-Data>'
UDA_count = 0
connection_count = 0

def convert_int_to_bytearray(num):
    hex_num = hex(num)
    hex_num = hex_num.replace('0x', '')
    if not (len(hex_num)%2 == 0):
        hex_num = '0' + hex_num
    return binascii.unhexlify(hex_num)

def handle_CER_CEA(hop_id, end_id):
    version = b'\x01'
    message_len = b'\x00\x00\xd0'
    flags = b'\x00'
    command_code = b'\x00\x01\x01'
    application_id = b'\x00\x00\x00\x00'
    result_code = b'\x00\x00\x01\x0c\x40\x00\x00\x0c\x00\x00\x07\xd1'
    origin_host = b'\x00\x00\x01\x08\x40\x00\x00\x17\x73\x70\x73\x2e\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62\x00'
    host_ip = b'\x00\x00\x01\x01\x40\x00\x00\x0e\x00\x01' + ipaddress.IPv4Address(LOCAL_HOST).packed + b'\x00\x00'
    origin_realm = b'\x00\x00\x01\x28\x40\x00\x00\x13\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62\x00'
    vendor_id = b'\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x65\x7b'
    product_name = b'\x00\x00\x01\x0d\x00\x00\x00\x0b\x53\x50\x53\x00'
    origin_state = b'\x00\x00\x01\x16\x40\x00\x00\x0c\x00\x00\x00\x00'
    supported_vendor = b'\x00\x00\x01\x09\x40\x00\x00\x0c\x00\x00\x28\xaf'
    auth_application_id = b'\x00\x00\x01\x02\x40\x00\x00\x0c\x01\x00\x00\x01'
    inband_security_id = b'\x00\x00\x01\x2b\x40\x00\x00\x0c\x00\x00\x00\x00'
    vendor_specific_app_id = b'\x00\x00\x01\x04\x40\x00\x00\x20\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x01\x02\x40\x00\x00\x0c\x01\x00\x00\x01'
    firmware_revision = b'\x00\x00\x01\x0b\x00\x00\x00\x0c\x00\x00\x00\x01'
    CEA = version + message_len + flags + command_code + application_id + hop_id + end_id + result_code + origin_host + host_ip + origin_realm + vendor_id + product_name + origin_state + supported_vendor + auth_application_id + inband_security_id + vendor_specific_app_id + firmware_revision
    return(CEA)

def handle_DWR_DWA(hop_id, end_id):
    version = b'\x01'
    message_len = b'\x00\x00\x58'
    flags = b'\x00'
    command_code = b'\x00\x01\x18'
    application_id = b'\x00\x00\x00\x00'
    result_code = b'\x00\x00\x01\x0c\x40\x00\x00\x0c\x00\x00\x07\xd1'
    origin_host = b'\x00\x00\x01\x08\x40\x00\x00\x17\x73\x70\x73\x2e\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62\x00'
    origin_realm = b'\x00\x00\x01\x28\x40\x00\x00\x13\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62\x00'
    origin_state = b'\x00\x00\x01\x16\x40\x00\x00\x0c\x00\x00\x00\x00'
    DWA = version + message_len + flags + command_code + application_id + hop_id + end_id + result_code + origin_host + origin_realm + origin_state
    return(DWA)

def handle_UDR_UDA(hop_id, end_id, session_id, user_id):
    global UDA_count
    global count_dict
    global user_data_dict
    UDA = ''
    version = b'\x01'
    flags = b'\x40'
    command_code = b'\x00\x01\x32'
    application_id = b'\x01\x00\x00\x01'
    len_session_id_AVP = len(session_id) + 8
    session_id_AVP = b'\x00\x00\x01\x07\x40\x00\x00' + convert_int_to_bytearray(len_session_id_AVP) + session_id
    if (len_session_id_AVP % 4 == 1):
        session_id_AVP += b'\x00\x00\x00'
    elif (len_session_id_AVP % 4 == 2):
        session_id_AVP += b'\x00\x00'
    elif (len_session_id_AVP % 4 == 3):
        session_id_AVP += b'\x00'
    udata_used = 'user_set_default'
    udata_from_range = user_data_dict[udata_used]
    user_data_found = False
    user_id_decode = user_id.decode()
    user_id_int = int(user_id_decode)
    for i in number_range_list:
        if ( user_id_int >= i[0] and user_id_int <= i[1]):
            udata_used = i[2][0]
            udata_from_range = i[2][1]
            user_data_found = True
            count_dict[udata_used] += 1
    if not user_data_found:
        count_dict[udata_used] += 1
    if not udata_from_range == b'NON_HOME':
        udata_8 = udata_2 + user_id + udata_3 + user_id + udata_4 + user_id + udata_5 + udata_6 + udata_from_range + udata_7
        user_data_len = len(b'\x00\x00\x02\xbe\xc0\x00\x00\x00' + udata_8 )
        user_data = udata_1 + convert_int_to_bytearray(user_data_len) + udata_8
        len_UDA = 3 + len(version + flags + command_code + application_id + hop_id + end_id + session_id_AVP + udr_vendor_specfic_app_id + udr_auth_session_state + udr_result_code + udr_origin_host + udr_origin_realm + user_data)
        if (len_UDA % 4 == 1):
            UDA_END = b'\x00\x00\x00'
            len_UDA += 3
        elif (len_UDA % 4 == 2):
            UDA_END = b'\x00\x00'
            len_UDA += 2
        elif (len_UDA % 4 == 3):
            UDA_END = b'\x00'
            len_UDA += 1
        UDA = version + b'\x00' + convert_int_to_bytearray(len_UDA) + flags + command_code + application_id + hop_id + end_id + session_id_AVP + udr_vendor_specfic_app_id + udr_auth_session_state + udr_result_code + udr_origin_host + udr_origin_realm + user_data + UDA_END
    else:
        len_UDA = 3 + len(version + flags + command_code + application_id + hop_id + end_id + session_id_AVP + b'\x00\x00\x01\x04\x40\x00\x00\x20\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x01\x02\x40\x00\x00\x0c\x01\x00\x00\x01\x00\x00\x01\x15\x40\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x01\x29\x40\x00\x00\x20\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x01\x2a\x40\x00\x00\x0c\x00\x00\x13\x89\x00\x00\x01\x08\x40\x00\x00\x17\x73\x70\x73\x2e\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62\x00\x00\x00\x01\x28\x40\x00\x00\x13\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62')
        if (len_UDA % 4 == 1):
            UDA_END = b'\x00\x00\x00'
            len_UDA += 3
        elif (len_UDA % 4 == 2):
            UDA_END = b'\x00\x00'
            len_UDA += 2
        elif (len_UDA % 4 == 3):
            UDA_END = b'\x00'
            len_UDA += 1
        UDA = version + b'\x00\x00' + convert_int_to_bytearray(len_UDA) + flags + command_code + application_id + hop_id + end_id + session_id_AVP + b'\x00\x00\x01\x04\x40\x00\x00\x20\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x01\x02\x40\x00\x00\x0c\x01\x00\x00\x01\x00\x00\x01\x15\x40\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x01\x29\x40\x00\x00\x20\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x01\x2a\x40\x00\x00\x0c\x00\x00\x13\x89\x00\x00\x01\x08\x40\x00\x00\x17\x73\x70\x73\x2e\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62\x00\x00\x00\x01\x28\x40\x00\x00\x13\x6d\x61\x76\x65\x6e\x69\x72\x2e\x6c\x61\x62' + UDA_END
    return(UDA)

async def diam_handler(reader, writer):
    global connection_count
    global failed
    global UDA_count
    connection_count += 1
    while True:
        try:
            data_read = await reader.readexactly(4)
            data_length = int(binascii.hexlify(data_read[1:4]), 16)
            data_read += await reader.readexactly(data_length-4)
            packet_type = data_read[5:8]
            hop_by_hop_id = data_read[12:16]
            end_to_end_id = data_read[16:20]
            if packet_type == b'\x00\x01\x01':
                CEA_packet = handle_CER_CEA(hop_by_hop_id,end_to_end_id)
                writer.write(CEA_packet)
                await writer.drain()
                print("CEA sent")
            elif packet_type == b'\x00\x01\x18':
                DWA_packet = handle_DWR_DWA(hop_by_hop_id, end_to_end_id)
                writer.write(DWA_packet)
                await writer.drain()
                print("DWA sent")
            elif packet_type == b'\x00\x01\x32':
                session_id_len = int(binascii.hexlify(data_read[25:28]),16)-8
                session_id = data_read[28:(28+session_id_len)]
                split_data = data_read.split(b'\x00\x00\x28\xaf\x00\x00\x02\xbd\xc0')
                user_id = split_data[1][7:18]
                UDA_packet = handle_UDR_UDA(hop_by_hop_id, end_to_end_id, session_id, user_id)
                if UDA_packet:
                    UDA_count += 1
                else:
                    failed += 1
                writer.write(UDA_packet)
                await writer.drain()
            else:
                print("Unknown packet type received. Ignoring and continuing to process next packet")
                continue
        except Exception as e:
            print("Exception: " + str(e))
            connection_count -= 1
            if connection_count == 0:
                print("resetting count")
                UDA_count = 0
                for i in count_dict.keys():
                    count_dict[i] = 0    
            writer.close()
            return

async def display():
    while True:
        await asyncio.sleep(5)
        print("Connection Count: " + str(connection_count))
        print("Total UDA count: " + str(UDA_count))
        print("Total FAIL count: " + str(failed))
        for i in count_dict.keys():
            print("                      " + str(i) + "-> " + str(count_dict[i]))


loop = asyncio.get_event_loop()

loop.create_task(display())
coro = asyncio.start_server(diam_handler, LOCAL_HOST, PORT, loop=loop)
server = loop.run_until_complete(coro)

failed = 0

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

