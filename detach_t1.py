#!/usr/bin/env python
# coding=utf-8

_author_ = 'mpinizzotto'


#Detach T1 gateway from T0 gateway

import requests
requests.packages.urllib3.disable_warnings() 
import json
from requests.auth import HTTPBasicAuth


headers = { 'content-type': 'application/json' }
username = 'admin'
password = 'VMware1!VMware1!'
t1_gw = 'T1-GW'
t0_gw = 'T0-GW-01'
nsxtmgr = "nsxtmgr01"
auth = HTTPBasicAuth(username, password)


def disconnect_t0(t1_gw):
    url = 'https://' + nsxtmgr + '/policy/api/v1/infra/tier-1s/' + t1_gw    
    payload = { "tier0_path": "None" }
    response = requests.patch(url, data=json.dumps(payload), headers=headers,  verify=False, auth=auth)
    return response

def main():
    response = disconnect_t0(t1_gw)
    #print response
    

if __name__ == '__main__':
    main()
