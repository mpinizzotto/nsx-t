#usr/bin/env python
#coding utf-8

_author_ = "mpinizzotto"

"""

pulls from csv file and deletes all existing tags

"""

import csv
import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

headers = { 'content-type': 'application/json' }
username = 'admin'
password = 'VMware1!VMware1!'
nsxtmgr = "nsxtmgr01"
auth = HTTPBasicAuth(username, password)


def get_current_config(config):
    vm_name = config.get('name')
    url = "https://" + nsxtmgr + "/api/v1/fabric/virtual-machines/?display_name=" + vm_name 
    response = requests.get(url, verify=False, auth=auth)
    parse = json.loads(response.text)
    external_id = parse['results'][0]['external_id']
    return external_id


def del_tags(external_id):
    url = "https://" + nsxtmgr + "/api/v1/fabric/virtual-machines?action=update_tags"
    
    payload =  {
        "external_id": external_id,
        "tags": [] 
    }   

    response = requests.post(url, data=json.dumps(payload), verify=False, auth=auth, headers=headers)
    return response


def read_from_csv(file):
    item_list = []
    csvfile = open(file, 'r')
    csv_in = csv.reader(csvfile)
    for item in csv_in:
        item_list.append(item)
    return item_list
    cvsfile.close()


def normalize_tag_list(item_list):
    tag_list = []
    for line in item_list:
        vm_info = {}
        vm_info['name']= line[0]
        vm_info['scope'] = line[1]
        vm_info['tag'] = line[2]  
        tag_list.append(vm_info)
    return tag_list


def main():
    item_list = read_from_csv('vm_tags.csv')
    tag_list = normalize_tag_list(item_list)

    for config in tag_list:
        external_id = get_current_config(config)
        response = del_tags(external_id)
        print response


if __name__ == '__main__':
    main()
