import asyncio
from re import findall

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()

LOCAL_HOST = file_lines[0].split('=')[1].strip()
LOCAL_PORT = int(file_lines[1].split('=')[1].strip())
REMOTE_HOST = file_lines[2].split('=')[1].strip()
REMOTE_PORT = int(file_lines[3].split('=')[1].strip())
IMAGE_FILE = file_lines[4].split('=')[1].strip()

async def handle_GET_msrp(reader, writer, data_read):
    global SUCCESS_COUNT
    global FAILED_COUNT
    try:
        HTTP_resp = 'HTTP/1.1 200 OK\r\n' \
                    'Server: mavenir\r\n' \
                    'Content-Type: image/png\r\n' \
                    'Content-Length: '
        HTTP_resp = HTTP_resp + str(FILE_DATA_MSRP_LEN) + '\r\n' \
                    'Connection: close\r\n' \
                    'Date: Fri, 29 Dec 2017 19:59:51 GMT\r\n\r\n' 

        HTTP_resp = HTTP_resp.encode() + FILE_DATA
        writer.write(HTTP_resp)
        await writer.drain()
        SUCCESS_COUNT += 1
        writer.close()
        return True
    except Exception as e:
        print("Exception: " + str(e))
        FAILED_COUNT += 1
        writer.close()
        return False

async def handle_HTTP(reader, writer):
    global SUCCESS_COUNT, FAILED_COUNT, GET_COUNT
    result = False
    try:
        data_read = await reader.readuntil(b'\r\n\r\n')
        GET_COUNT += 1
        if b'GET /mStoreRoot/file' in data_read:
            result = await handle_GET_msrp(reader, writer, data_read)
        else:
            print("Unexpected message")
    except Exception as e:
        print("Exception occured")
    finally:
        print("GET: " + str(GET_COUNT))
        print("SUCCESS: " + str(SUCCESS_COUNT))
        print("FAIL: " + str(FAILED_COUNT))
        return

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_HTTP, LOCAL_HOST, LOCAL_PORT, loop=loop)
server = loop.run_until_complete(coro)

SUCCESS_COUNT = 0
GET_COUNT = 0
FAILED_COUNT = 0
FILE_DATA = open(IMAGE_FILE, 'rb').read()
FILE_DATA_MSRP_LEN = len(FILE_DATA)

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


