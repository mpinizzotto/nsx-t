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


def get_t1_config():
  url = 'https://' + nsxtmgr + '/policy/api/v1/infra/tier-1s/' + t1_gw  
  response = requests.get(url, verify=False, auth=auth)
  current_config = json.loads(response.text)
  return current_config

def check_config_state(current_config):
    if 'tier0_path' in current_config:
        if current_config['tier0_path'] == '/infra/tier-0s/' + t0_gw:
            return False
        else:
            return True
    else:
        return True

def attach_t0():
    url = 'https://' + nsxtmgr + '/policy/api/v1/infra/tier-1s/' + t1_gw    
    payload = { "tier0_path": '/infra/tier-0s/' + t0_gw }
    response = requests.patch(url, data=json.dumps(payload), headers=headers,  verify=False, auth=auth)
    return response

def main(): 
    current_config = get_t1_config()
    t1_state = check_config_state(current_config)
    if t1_state  == True:
        response = attach_t0()
        print response.status_code
    else:
        pass


if __name__ == '__main__':
    main()



