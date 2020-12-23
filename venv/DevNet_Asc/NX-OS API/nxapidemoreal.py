import requests
import json
import re

switchuser = 'cisco'
switchpassword ='cisco'

url = 'https://172.16.1.68/ins'
myheader = {'content-type':'application/json'}
payload = {
    "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show cdp nei",
        "output_format": "json"
    }
}

response = requests.post(url, data=json.dumps(payload),headers=myheader, auth=(switchuser,switchpassword),verify=False).json()
print(response)
##################################
auth_url = 'https://172.16.1.68/api/mo/aaaLogin.json'
auth_body = {"aaaUser":{"attributes":{
    "name": switchuser, "pwd:": switchpassword}}}

auth_reponse = requests.post(auth_url,body=json.dumps(auth_body),timeout=5,verify=False).json()
token = auth_reponse['imdata'][0]['aaaLogin']['attributes']['token']
cookies={}
cookies['APIC-cookie']=token

counter = 0
nei_count = response['ins_api']['outputs']['output']['body']['neigh_count']

while counter < nei_count:
    hostname = response['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_info'][counter]['device_id']
    local_int = ['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_info'][counter]['device_id']
    remote_int = ['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_info'][counter]['device_id']

body = {
    "l1PhysIf": {
        "attributes":{
            "descr": 'Connected to '+hostname+' Remote int is '+remote_int
        }
    }
}

counter += 1

if local_int != 'mgmt0':
    int_name = str.lower(str(local_int[:3]))
    int_num = re.search(r'[1-9]/[1-9]*', local_int)
    int_url = 'https://172.16.1.68/api/mo/sys/intf/phys-['+int_name+str(
        int_num.group(0))+'].json'
    post_response = requests.post(int_url, data=json.dump(body), headers=myheader, cookies=cookies, verify=False).json()
    print(post_response)