from aiohttp import web
from re import findall
from asyncio import sleep

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()

LOCAL_HOST = file_lines[0].split('=')[1].strip()
LOCAL_PORT = int(file_lines[1].split('=')[1].strip())
REMOTE_HOST = file_lines[2].split('=')[1].strip()
REMOTE_PORT = int(file_lines[3].split('=')[1].strip())

display_task_started = False
GET_200 = 0

async def display_count():
    while True:
        await sleep(5)
        print("GET_200 : " + str(GET_200))

async def handle_get(request):
    global display_task_started, GET_200
    if not display_task_started:
        print("Display started")
        app.loop.create_task(display_count())
        display_task_started = True
    req_url = str(request.url)
    destNum = findall('/abc/1(\d{10})', req_url)
    destNum = destNum[0]
    response_final = '{\r\n' \
                  '"Trunk":[\r\n' \
                  '{\r\n' \
                  '"MDN":"1' + destNum + \
                  '",\r\n"feature":"VLT,RCS,RMH,RMD,RFT,EAB,LVC,UCA",\r\n' \
                  '"Charging-Group":"131",\r\n' \
                  '"rcs_state":"ENABLED",\r\n' \
                  '"suspended":"False",\r\n' \
                  '"IMEI":"1234' + destNum + '"\r\n}\r\n]\r\n}'
    GET_200 += 1
    return web.Response(status=200, body=response_final, content_type='application/json')

app = web.Application()
app.add_routes([web.get('/abc/{info}', handle_get)])
web.run_app(app, host=LOCAL_HOST, port=LOCAL_PORT)
