import sys
import os
import json
import nmapscan, msf
import dirb, whatweb, zaproxy, bruteforce

with open('../Scripts/config.json') as json_data_file:
    config = json.load(json_data_file)

def network(target):
    # Workaround for demo purposes. Network scan doesn't work with http://
    retdata = {}
    host = "127.0.0.1"
    if "http" in target:
        target = target[target.index('://')+3:]
        print(target)
    #print("Start network scanning")
    retdata["ip"] = target
    nmapdata = nmapscan.initiate(target)
    retdata["nmapdata"] = nmapdata
    if nmapdata is None:
        #print('Nmap scan returned no open ports.')
        sys.exit()
    target = config['MSFRPC']['exploitip']
    
    retdata["msfdata"] = msf.initiate(nmapdata, target, host)
    return retdata

def webapp(host):
    if not 'http' in host:
        #print('Invalid URL format: {0}'.format(host))
        #print('Use \'http://target\' or \'https://target\'')
        sys.exit()
    #print("Started webapp scanning")
    whatweb.initiate(host)
    links = dirb.initialize(host)
    #print(links)
    zaproxy.initialize(host)
    for link in links:
        if bruteforce.check_login_form(links):
            print(link)
            # Bruteforce these links manually with hydra or BurpSuite