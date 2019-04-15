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
    retdata["ip"] = target
    nmapdata = nmapscan.initiate(target)
    retdata["nmapdata"] = nmapdata
    if nmapdata is None:
        sys.exit()
    target = config['MSFRPC']['exploitip']
    
    retdata["msfdata"] = msf.initiate(nmapdata, target, host)
    return retdata

def webapp(host):
    if not 'http' in host:
        sys.exit()
    whatweb.initiate(host)
    links = dirb.initialize(host)
    zaproxy.initialize(host)
    
    linkid=0
    print("{")
    for link in links:
        print("'{}':'{}',".format(linkid, link))
        linkid = linkid + 1
            # Bruteforce these links manually with hydra or BurpSuite
    print("}")