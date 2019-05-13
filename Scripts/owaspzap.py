from time import sleep
from pprint import pprint
import json
from pathlib import Path
from zapv2 import ZAPv2
from loginauthmethod import loginauthmethod

with open(Path('../Scripts/config.json'), 'r') as f:
        config = json.load(f)

class owaspzap():
    key = config['ZAProxy']['key']
    zap = ZAPv2(apikey=key)
    contextname = None
    contextid = None
    userid = None
    authisset = False
    target = None
    loginurl = None
    username = None
    password = None
    authmethod = loginauthmethod.NONE
    authmethodname = None
    authmethodconfigparams = None
    contextregex = None
    loggedinindicator = None
    loggedoutindicator = None
    credentials = None
    scanid = None

    def initialize(self, contextname, target, contextregex):
        self.contextname = contextname
        self.zap = ZAPv2(apikey=self.key)
        self.zap.core.new_session(apikey=self.key)
        self.contextid = self.zap.context.new_context(contextname=self.contextname, apikey=self.key)

        self.target = target
        self.contextregex = contextregex

        if(self.zap.core.alerts()):
            self.zap.core.delete_all_alerts(apikey=self.key)    
        self.zap.context.include_in_context(self.contextname, self.contextregex, apikey=self.key)
        
        self.zap.urlopen(self.target)

    def authenticate(self, loginurl, username, password, loggedinindicator, loggedoutindicator, authmethod):
        if(authmethod != loginauthmethod.NONE):
            self.loginurl = loginurl
            self.username = username
            self.password = password
            self.authmethod = authmethod
            self.loggedinindicator = loggedinindicator
            self.loggedoutindicator = loggedoutindicator
            
            #self.authmethodconfigparams = "loginUrl={0}&loginRequestData=username%3D%7B%25{1}%25%7D%26password%3D%7B%25{2}%25%7D".format(loginurl, username, password)
            self.authmethodconfigparams = "hostname={0}&realm={1}&port=80".format(loginurl, "Secret page")

            self.authmethodname = self.authmethod.value
            self.zap.authentication.set_authentication_method(self.contextid, self.authmethodname, authmethodconfigparams=self.authmethodconfigparams, apikey=self.key)
            self.zap.authentication.set_authentication_method
            self.zap.authentication.set_logged_in_indicator(self.contextid, self.loggedinindicator, apikey=self.key)
            self.zap.authentication.set_logged_out_indicator(self.contextid, self.loggedoutindicator, apikey=self.key)
            self.userid = self.zap.users.new_user(self.contextid, self.username, apikey=self.key)
            self.credentials = "username={0}&password={1}".format(self.username, self.password)
            self.zap.users.set_authentication_credentials(self.contextid, self.userid, self.credentials, apikey=self.key)
            self.zap.users.set_user_enabled(self.contextid, self.userid, "true", apikey=self.key)
            self.zap.forcedUser.set_forced_user_mode_enabled(True, apikey=self.key)

            self.authisset = True

        else:
            print("Please specify authmethod.")


    def spider(self, target):
        if(self.authisset):
            self.scanid = self.zap.spider.scan_as_user(self.contextid, self.userid, url=target)
        else:
            self.scanid = self.zap.spider.scan(url=target, contextname=self.contextname)
        
        sleep(2)

        while (int(self.zap.spider.status(self.scanid)) < 100):
            sleep(2)
    
    def passive_scan(self):
        while (int(self.zap.pscan.records_to_scan) > 0):
            sleep(2)
    
    def active_scan(self, target):
        self.scanid = self.zap.ascan.scan(target)
        sleep(2)
        while (int(self.zap.ascan.status(self.scanid)) < 100):
            sleep(5)

    def get_alerts(self):
        return json.dumps(self.zap.core.alerts())
    
    def get_spider(self):
        return (self.zap.spider.full_results(self.scanid))

    def context_remove(self):
        self.zap.context.remove_context(self.contextname, apikey=self.key)

    def __str__(self):
        return ("ContextName: " + str(self.contextname) + 
            ", ContextId: " + str(self.contextid) + 
            ", UserId: " + str(self.userid) + 
            ", AuthIsSet: " + str(self.authisset) + 
            ", Key: " + str(self.key) + 
            ", Zap: " + str(self.zap) +
            ", Target: " + str(self.target) +
            ", LoginUrl: " + str(self.loginurl) + 
            ", Username: " + str(self.username) + 
            ", Password: " + str(self.password) + 
            ", AuthMethod: " + str(self.authmethod.value) +
            ", AuthMethodConfigParams: " + str(self.authmethodconfigparams) +
            ", ContextRegex: " + str(self.contextregex) + 
            ", LoggedInIndicator: " + str(self.loggedinindicator) + 
            ", LoggedOutIndicator: " + str(self.loggedoutindicator) + 
            ", Credentials: " + str(self.credentials) + 
            ", ScanId: " + str(self.scanid)
        )