#!/usr/bin/env python
# coding=utf-8

_author_ = 'mpinizzotto'


#Detach T1 gateway from T0 gateway


import requests
import json
from requests.auth import HTTPBasicAuth

username = 'admin'
password = 'VMware1!VMware1!'
t1_gw = 'T1-GW'
t0_gw = 'T0-GW-01'
nsxtmgr = "nsxtmgr01"
auth = HTTPBasicAuth(username, password)
headers = { 'content-type': 'application/json' }

def disconnect_t0():
    url = 'https://' + nsxtmgr + '/policy/api/v1/infra/tier-1s/' + t1_gw    
    payload = { "tier0_path": "None" }
    response = requests.patch(url, data=json.dumps(payload), headers=headers,  verify=False, auth=auth)
    return response

if __name__ == '__main__':

    rc = disconnect_t0()
    print rc.status_code

