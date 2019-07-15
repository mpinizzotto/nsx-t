

####################################
#
###################################

import requests
import json
from requests.auth import HTTPBasicAuth

headers = { 'content-type': 'application/json' }
username = 'admin'
password = 'VMware1!VMware1!'
t1_gw = 'T1-GW'
t0_gw = 'T0-GW-01'
nsxtmgr = "nsxtmgr01"
auth = HTTPBasicAuth(username, password)


def get_t0_path():
  url = 'https://nsxtmgr01/policy/api/v1/infra/tier-0s/' + t0_gw  
  response = requests.get(url, verify=False, auth=auth)
  parse = json.loads(response.text)
  t0_path = parse['path']
  return t0_path

def attach_t0(t0_path):
    url = 'https://' + nsxtmgr + '/policy/api/v1/infra/tier-1s/' + t1_gw    
    payload = { "tier0_path": "" + t0_path + "" }
    response = requests.patch(url, data=json.dumps(payload), headers=headers,  verify=False, auth=auth)
    return response

if __name__ == '__main__':

    t0_path = get_t0_path()
    rc = attach_t0(t0_path)
    print rc.status_code

