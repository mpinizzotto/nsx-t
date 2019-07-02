#!/usr/bin/env python
# coding=utf-8

_author_ = "mpinizzotto"

# Updates Global Switching MTU for NSX-T 2.4.X

import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

nsxmanager = '192.168.110.26'
username = 'admin'
password = 'VMware1!VMware1!'
mtu = '1600'
auth = HTTPBasicAuth( username, password)
headers = {
    'Content-Type': 'application/json'
}

def get_config():
    url = 'https://' + nsxmanager + '/api/v1/global-configs/SwitchingGlobalConfig'
    response = requests.get(url, headers=headers, verify=False, auth=auth)
    parse = json.loads(response.text)
    current_revision = parse['_revision']
    current_mtu = parse['physical_uplink_mtu']
    return current_revision, current_mtu
	
def update_config(current_revision):
    mtu_payload = {
      "_revision": current_revision,
      "resource_type": "SwitchingGlobalConfig",
      "physical_uplink_mtu": mtu
    }
    
    url = 'https://' + nsxmanager + '/api/v1/global-configs/SwitchingGlobalConfig?action=resync_config'
    response = requests.put(url, data=json.dumps(mtu_payload), headers=headers, verify=False, auth=auth)
    parse = json.loads(response.text)
    updated_mtu = parse['physical_uplink_mtu']
    return updated_mtu


if __name__ == "__main__":
    
    print ""
    print "Setting Global Switching MTU........."
    
    current_revision, current_mtu = get_config()
    updated_mtu = update_config(current_revision)
    
    print "Global MTU: ", updated_mtu







