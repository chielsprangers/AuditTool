from time import sleep
from pprint import pprint
import json
from pathlib import Path
from zapv2 import ZAPv2

with open(Path('../Scripts/config.json'), 'r') as f:
    config = json.load(f)

key = config['ZAProxy']['key']
zap = ZAPv2(apikey=key)

def initialize(host):
    # zap = ZAPv2(apikey=key)
    try:
        zap.urlopen(host)
        sleep(2)
        spider(host)
        passive_scan()
        active_scan(host)
        return get_alerts()
    except:
        print('WARNING: Make sure Zaproxy is running in Daemon mode with the designated key: {0}'.format(key))

def authentication(loginUrl):
    print("placeholder")
	# from zapv2 import ZAPv2
    # context = 'new_attack'
    # authmethodname = 'formBasedAuthentication'
    # authmethodconfigparams = "".join('loginUrl=https://192.168.0.1/dologin.html' '&loginRequestData=username%3D%7B%25username%25%7D%26' 'password%3D%7B%25password%25%7D')
    # target = 'https://192.168.0.1'
    # apikey = 'password'
    # zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8119', 'https': 'http://127.0.0.1:8119'}, apikey=apikey)

    # contextid = zap.context.new_context(context)
    # print contextid
    # print zap.context.include_in_context(context, 'https://192.168.0.1.*')

    # print zap.context.context(context)

    # print zap.authentication.set_authentication_method(contextid, authmethodname, authmethodconfigparams)
    # # The indicators should be set after setting the authentication method.
    # print zap.authentication.set_logged_in_indicator(contextid, loggedinindicatorregex='Logged in')
    # print zap.authentication.set_logged_out_indicator(contextid, 'Sorry, the username or password you entered is incorrect')

    # userid = zap.users.new_user(contextid, 'User 1')
    # print userid
    # print zap.users.set_authentication_credentials(contextid, userid, 'username=MyUserName&password=MySecretPassword')
    # print zap.users.set_user_enabled(contextid, userid, True)

    # print zap.spider.scan_as_user(contextid, userid, target)*/


def spider(host):
    scanid = zap.spider.scan(host)
    sleep(2)
    while (int(zap.spider.status(scanid)) < 100):
        print('Spider progress %: {}'.format(zap.spider.status(scanid)))
        sleep(2)
    print('Spider completed')
    return scanid

def passive_scan():
    while (int(zap.pscan.records_to_scan) > 0):
        print('Records to passive scan: {}'.format(zap.pscan.records_to_scan))
        sleep(2)
    print('Passive scan completed')

def active_scan(host):
    print('Active scanning target {}'.format('host'))
    scanid = zap.ascan.scan(host)
    sleep(2)
    while (int(zap.ascan.status(scanid)) < 100):
        print('Scan progress %: {}'.format(zap.ascan.status(scanid)))
        sleep(5)
    print('Active scan completed')

def get_alerts():
    print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    print('Alerts: ')
    pprint(zap.core.alerts())
    return zap.core.alerts()
