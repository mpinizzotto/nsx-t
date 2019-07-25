#!/usr/bin/env python
# coding=utf-8

_author_ = 'mpinizzotto'

# Attaches T1 gateway to T0 gateway


import json
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings() 

headers = { 'content-type': 'application/json' }
username = 'admin'
password = 'VMware1!VMware1!'
t1_gw = 'T1-GW'
t0_gw = 'T0-GW-01'
nsxtmgr = "nsxtmgr01"
auth = HTTPBasicAuth(username, password)


def attach_t0():
    url = 'https://' + nsxtmgr + '/policy/api/v1/infra/tier-1s/' + t1_gw    
    payload = { "tier0_path": '/infra/tier-0s/' + t0_gw }
    response = requests.patch(url, data=json.dumps(payload), headers=headers,  verify=False, auth=auth)
    return response

def main(): 
    response = attach_t0()
    #print response.status_code


if __name__ == '__main__':
    main()



