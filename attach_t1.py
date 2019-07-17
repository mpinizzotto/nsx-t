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


def get_t0_config(t0_gw):
  url = 'https://nsxtmgr01/policy/api/v1/infra/tier-0s/' + t0_gw  
  response = requests.get(url, verify=False, auth=auth)
  current_config = json.loads(response.text)
  return current_config

def attach_t0(t0_path):
    url = 'https://' + nsxtmgr + '/policy/api/v1/infra/tier-1s/' + t1_gw    
    payload = { "tier0_path": "" + t0_path + "" }
    response = requests.patch(url, data=json.dumps(payload), headers=headers,  verify=False, auth=auth)
    return response

def main(): 
    t0_config = get_t0_config(t0_gw)
    t0_path = t0_config['path']
    response = attach_t0(t0_path)
    print response.status_code


if __name__ == '__main__':
    main()



