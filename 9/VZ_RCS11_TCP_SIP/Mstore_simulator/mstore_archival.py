from aiohttp import web
from random import randint

file_obj = open("conf.txt", 'r')
file_lines = file_obj.readlines()

LOCAL_HOST = file_lines[0].split('=')[1].strip()
LOCAL_PORT = int(file_lines[1].split('=')[1].strip())
HEALTH_PING_STRING = file_lines[2].split('=')[1].strip()
ARCHIVE_STRING = file_lines[3].split('=')[1].strip()
VM_STRING = file_lines[4].split('=')[1].strip()
FAX_STRING = file_lines[5].split('=')[1].strip()

health_ping_count = 0
archival_count = 0
vm_count = 0
fax_count = 0

async def post_handler_health_ping(request):
    global health_ping_count
    health_ping_count += 1
    print("Health: " + str(health_ping_count) + " Store: " + str(archival_count) + " VM: " + str(vm_count) + " FAX: " + str(fax_count))
#    if request.body_exists:
#       await request.read()
    return web.Response()

async def post_handle_archive(request):
    global archival_count
    archival_count += 1
    print("Health: " + str(health_ping_count) + " Store: " + str(archival_count) + " VM: " + str(vm_count) + " FAX: " + str(fax_count))
#    if request.body_exists:
#        data = await request.read()    
    tel_number = request.match_info['number']
    url = 'http://'+ str(LOCAL_HOST) + ':' + str(LOCAL_PORT) + '/rmsclient/nms/v1/rms/tel%3a%2b' + str(tel_number) + '/objects/' + str(randint(0000,9999)) + 'aaa-e7f5-48da-b5bf-ee310c' + str(randint(0000,9999)) + 'bc%3a' + str(randint(0000,9999)) 
    rsp_json = {"objectReference":{"resourceURL":url}}
    return web.json_response(rsp_json, status=201)

async def post_handler_vmSync(request):
    global vm_count
    vm_count += 1
    print("Health: " + str(health_ping_count) + " Store: " + str(archival_count) + " VM: " + str(vm_count) + " FAX: " + str(fax_count))
#    if request.body_exists:
#        await request.read()
    return web.Response()

async def post_handler_fax(request):
    global fax_count
    fax_count += 1
    print("Health: " + str(health_ping_count) + " Store: " + str(archival_count) + " VM: " + str(vm_count) + " FAX: " + str(fax_count))
#    if request.body_exists:
#        await request.read()
    tel_number = request.match_info['number']
    url = 'http://'+ str(LOCAL_HOST) + ':' + str(LOCAL_PORT) + '/host/nms/v1/ums/tel%3a%2b' + str(tel_number) + '/objects/' + str(randint(0000,9999)) + 'fff-e7f5-48da-b5bf-ee310c' + str(randint(0000,9999)) + 'bc%3a' + str(randint(0000,9999))
    rsp_json = {"objectReference":{"resourceURL":url}}
    return web.json_response(rsp_json, status=201)

app = web.Application()
app.add_routes([web.post(HEALTH_PING_STRING, post_handler_health_ping),
                web.post(ARCHIVE_STRING, post_handle_archive),
                web.post(VM_STRING, post_handler_vmSync),
                web.post(FAX_STRING, post_handler_fax)])

web.run_app(app, host=LOCAL_HOST, port=LOCAL_PORT)
