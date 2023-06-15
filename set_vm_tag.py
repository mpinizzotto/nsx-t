#usr/bin/env python
#coding utf-8

import csv
import sys
import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

_author_ = "mpinizzotto"

"""
pulls from csv file (name, scope, tag), adds tags to virtual machine.

python set_vm_tag.py myfile.csv

"""

headers = {'content-type': 'application/json'}
username = 'admin'
password = 'mypassword'
nsxtmgr = "nsxmgr.local"
auth = HTTPBasicAuth(username, password)
file = sys.argv[1]

def get_config(line):
    vm_name = line.get('name')
    url = "https://" + nsxtmgr + "/api/v1/fabric/virtual-machines/?display_name=" + vm_name
    response = requests.get(url, verify=False, auth=auth)
    parse = json.loads(response.text)
    external_id = parse['results'][0]['external_id']
    if 'tags' in parse['results'][0]:
        current_tags = parse['results'][0]['tags']
    else:
        current_tags = None
    return external_id, current_tags, vm_name


def update_tags(external_id, line, current_tags):
    new_tags = []
    line.pop('name')
    new_tags.append(line)
    if current_tags is not None:
        for tags in current_tags:
            new_tags.append(tags)
    else:
        pass
    url = "https://" + nsxtmgr + "/api/v1/fabric/virtual-machines?action=add_tags"
    payload = {
        "external_id": external_id,
        "tags": new_tags
    }
    response = requests.post(url, data=json.dumps(payload), verify=False, auth=auth, headers=headers)
    return response, new_tags

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
        if line == []:
            continue
        else:
            vm_info = {}
            vm_info['name'] = line[0]
            vm_info['scope'] = line[1]
            vm_info['tag'] = line[2]
            tag_list.append(vm_info)
    return tag_list

def main():
    item_list = read_from_csv(file)
    tag_list = normalize_tag_list(item_list)
    print ""
    for line in tag_list:
        external_id, current_tags, vm_name = get_config(line)
        response, new_tags = update_tags(external_id, line, current_tags)
        print "Added " + vm_name + ": "+ new_tags[0]["scope"]+":"+new_tags[0]["tag"]
    print ""

if __name__ == '__main__':
    main()
