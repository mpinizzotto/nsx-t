#usr/bin/env python
#coding utf-8


"""
Pulls data from .csv file and creates vRNI application with IP address criteria

    CVS format - required for running this script    
    app_name, tier_name, ip_addr      
    "app1","tier1","10.10.10.0/24"
    "app2","tier1","10.20.10.0/24"
    
App name and tier name do not support special characters 
"""
    
#TODO: update normalization definition to check for special characters in name strings
#  as well as support mulitple ip addresses

_author_ = "mpinizzotto"

import re
import csv
import requests
import json
requests.packages.urllib3.disable_warnings()


headers = { 'content-type': 'application/json' }

"""
update these variables 
"""
username = 'admin@local'
password = 'mypassword'
vrni = "vrni.local"
file = "myfile.csv"


def check_current_app(app_name, token_header):
    filter = "name = {}".format(app_name)
    payload = { "entity_type": "Application", "filter": filter }
    url = "https://" + vrni + "/api/ni/search"
    response = requests.post(url, data=json.dumps(payload), verify=False, headers=token_header)
    parse = json.loads(response.text)
    if parse['results'] == []:
        return False
    else:
        return True

def create_application(app_name,token_header):
    url = "https://" + vrni + "/api/ni/groups/applications/"
    payload =  { "name" : app_name }
    response = requests.post(url, data=json.dumps(payload), verify=False, headers=token_header)
    parse = json.loads(response.text)
    entity_id = parse
    return entity_id['entity_id']

def create_app_tiers(entity_id,ip_addr,tier_name,token_header):
    url = "https://" + vrni + "/api/ni/groups/applications/" + entity_id + "/tiers"
    tier_payload = {
            "name": "dummy_name",
            "entity_type": "Tier",
            "group_membership_criteria": [
                {
                 "membership_type": "IPAddressMembershipCriteria",
                 "ip_address_membership_criteria": {"ip_addresses": []}
                }
            ]
        }
    ips = []
    if ip_addr is not None:
        ips.append(ip_addr)
        for ip in ips:
            if re.search("^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$", ip) or \
                        ("^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2})$", ip):
                valid_ips = True
    if not tier_name:
        tier_name = "Tier1"

    if valid_ips == True:
        tier_payload['name'] = tier_name
        tier_payload['group_membership_criteria'][0]['ip_address_membership_criteria']['ip_addresses'] = ips
        #print tier_payload
        response = requests.post(url, data=json.dumps(tier_payload), verify=False, headers=token_header)
        parse = json.loads(response.text)
        return parse
    else:
        print "Missing IP address"


def read_from_csv(file):
    item_list = []
    csvfile = open(file, 'r')
    csv_in = csv.reader(csvfile)
    for item in csv_in:
        item_list.append(item)
    return item_list
    cvsfile.close()

def normalize_app_list(item_list):
    app_list = []
    for line in item_list:
        app_info = {}
        app_info['name']= line[0]
        app_info['tier_name'] = line[1]
        app_info['ip_addr'] = line[2]
        app_list.append(app_info)
    return app_list

def get_auth_token(username,password):
    url = "https://" + vrni + "/api/ni/auth/token"
    payload =  {
                   "username" : username,
                   "password": password,
                   "domain": {
                       "domain_type": "LOCAL"
                   }
                }
    response = requests.post(url, data=json.dumps(payload), verify=False, auth=auth, headers=headers)
    parse = json.loads(response.text)
    token = parse['token']
    return token


def main():
    url = "https://" + vrni + "/api/ni/auth/token"
    payload =  {
                   "username" : username,
                   "password": password,
                   "domain": {
                       "domain_type": "LOCAL"
                   }
                }
    response = requests.post(url, data=json.dumps(payload), verify=False,  headers=headers)
    parse = json.loads(response.text)
    token = parse['token']
    token_header = {'Content-Type': 'application/json',
                    'Authorization': 'NetworkInsight {}'.format(token)}

    item_list = read_from_csv(file)
    app_list = normalize_app_list(item_list)

    for line in app_list:
        app_name = line.get("name")
        ip_addr = line.get("ip_addr")
        tier_name = line.get("tier_name")
       
	    is_app = check_current_app(app_name, token_header)
        if is_app == True:
            print "Skipping " + app_name + ",already created "
        if is_app == False:
            entity_id = create_application(app_name,token_header)
            print "Creating Application..." , app_name
            response =  create_app_tiers(entity_id,ip_addr,tier_name,token_header)
            print "App Name: ", app_name
            print "Tier Name: ", response['name']
            print "IP Address: ", response['group_membership_criteria'][0]['ip_address_membership_criteria']['ip_addresses'][0]
        else:
            continue


if __name__ == '__main__':
    main()
