import sys
import os
import json
from datetime import datetime
import nmapscan, msf
import dirb, whatweb, zaproxy, bruteforce
from owaspzap import owaspzap
from loginauthmethod import loginauthmethod

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
    
    target = "http://192.168.2.131/dvwa/"
    loginurl = "http://192.168.2.131/dvwa/login.php"
    username = "qwer"
    password = "1234"
    contextregex = "\Qhttp://192.168.2.131/dvwa\E.*"
    authmethod = loginauthmethod.FORM_BASED_AUTHENTICATION
    loggedinindicator = "Ingelogd!!!"
    loggedoutindicator = "Wrong username or password"

    zap = owaspzap()


    zap.initialize(str(datetime.now()), target, contextregex)
    zap.authenticate(loginurl, username, password, loggedinindicator, loggedoutindicator, authmethod)
    zap.spider(target)
    zap.passive_scan()
    zap.active_scan(target)
    print(zap.get_alerts())


    #print(str(zap))
    zap.context_remove()
    