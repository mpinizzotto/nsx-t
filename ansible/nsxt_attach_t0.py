#!/usr/bin/env python

import json
import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec
from ansible.module_utils.urls import open_url, fetch_url
from ansible.module_utils._text import to_native
from ansible.module_utils.six.moves.urllib.error import HTTPError


def get_t1_config(manager_url, mgr_username, mgr_password, validate_certs, t1_gateway):
  url = manager_url + '/infra/tier-1s/' + t1_gateway
  response = requests.get(url, headers={ 'content-type': 'application/json' }, verify=validate_certs, auth=HTTPBasicAuth(mgr_username, mgr_password))
  current_config = json.loads(response.text)
  return current_config


def check_config_state(current_config, t0_gateway):
    if 'tier0_path' in current_config:
        if current_config['tier0_path'] == '/infra/tier-0s/' + t0_gateway:
            return False
        else:
            return True
    else:
        return True


def attach_t0(manager_url, mgr_username, mgr_password, validate_certs, t1_gateway, t0_gateway):
    url = manager_url + '/infra/tier-1s/' + t1_gateway
    payload = { "tier0_path": '/infra/tier-0s/' + t0_gateway }
    response = requests.patch(url, data=json.dumps(payload), headers={ 'content-type': 'application/json' }, verify=validate_certs, auth=HTTPBasicAuth(mgr_username, mgr_password))
    return response


def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(t0_gw=dict(required=True, type='str'),
                         t1_gw=dict(required=True, type='str'))
    
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    mgr_hostname = module.params['hostname']
    mgr_username = module.params['username']
    mgr_password = module.params['password']
    validate_certs = module.params['validate_certs']
    manager_url = 'https://{}/policy/api/v1'.format(mgr_hostname)
    t0_gateway = module.params['t0_gw']
    t1_gateway = module.params['t1_gw']
    
    try:
        changed = False
        current_config = get_t1_config(manager_url, mgr_username, mgr_password, validate_certs, t1_gateway)
        t1_state = check_config_state(current_config, t0_gateway)
        
        if t1_state == True:
            response = attach_t0(manager_url, mgr_username, mgr_password, validate_certs, t1_gateway, t0_gateway)
            changed = True
            module.exit_json(changed=changed)
        else:
            changed = False
            module.exit_json(changed=changed)
			
    except Exception as err:
        module.fail_json(msg='Error accessing NSX Manager. Error [%s]' % (to_native(err)))
		
    module.exit_json(changed=changed)


if __name__ == '__main__':
	main()
