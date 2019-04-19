from time import sleep
from pprint import pprint
import json
from pathlib import Path
from zapv2 import ZAPv2

with open(Path('../Scripts/config.json'), 'r') as f:
    config = json.load(f)

key = config['ZAProxy']['key']
zap = ZAPv2(apikey=key)
authIsSet = False
contextname = ""
contextid = None
userid = None

def initialize(host):
    contextname = "appels"
    contextid = zap.context.new_context(contextname, apikey=key)
    print (contextid)
    
    try:
        zap.core.delete_all_alerts(apikey=key)
        zap.urlopen(host)
        sleep(2)
        authentication("test")
        spider(host)
        passive_scan()
        active_scan(host)
        
        return get_alerts()
    except Exception as e:
        print (e)
        zap.context.remove_context(contextname, apikey=key)
        print('WARNING: Make sure Zaproxy is running in Daemon mode with the designated key: {0}'.format(key))

def authentication(loginUrl):
    authmethodname = 'formBasedAuthentication'
    authmethodconfigparams = "".join('loginUrl=https://192.168.2.131/dvwa/login.php' '&loginRequestData=username%3D%7B%25username%25%7D%26' 'password%3D%7B%25password%25%7D')

    print ("<br/>AA1" + zap.context.include_in_context(contextname, 'https%3A%2F%2F192.168.2.131%2Fdvwa%2F%2A', apikey=key))
    print("<br/>")
    print("contextname:  " + contextname)
    print("<br/>")
    print("contextid: " + contextid)
    print("<br/>")
    print ("<br/>AA1.5")
    print ("<br/>AA2" + zap.context.context(contextname))
    print ("<br/>AA2.5")
    print ("<br/>AA3" + zap.authentication.set_authentication_method(contextid, authmethodname, authmethodconfigparams))

    print ("<br/>AA4" + zap.authentication.set_logged_in_indicator(contextid, loggedinindicatorregex='Ingelogd!!!'))
    print ("<br/>AA5" + zap.authentication.set_logged_out_indicator(contextid, 'Wrong username or password'))

    userid = zap.users.new_user(contextid, 'User 1')
    print ("<br/>AA6" + userid)
    print ("<br/>AA7" + zap.users.set_authentication_credentials(contextid, userid, 'username=admin&password=password'))
    print ("<br/>AA8<br/>" + zap.users.set_user_enabled(contextid, userid, True))


def spider(host):
    scanid = None
    if(authIsSet):
        scanid = zap.spider.scan_as_user(contextid, userid, host)
    else:
        scanid = zap.spider.scan(host)
    sleep(2)
    while (int(zap.spider.status(scanid)) < 100):
        sleep(2)
    return scanid

def passive_scan():
    while (int(zap.pscan.records_to_scan) > 0):
        sleep(2)

def active_scan(host):
    scanid = zap.ascan.scan(host)
    sleep(2)
    while (int(zap.ascan.status(scanid)) < 100):
        sleep(5)

def get_alerts():
    print('Alerts: ')
    for alert in zap.core.alerts():
        print("{},".format(alert))
    return zap.core.alerts()
    
