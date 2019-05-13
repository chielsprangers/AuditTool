from datetime import datetime
from owaspzap import owaspzap
from loginauthmethod import loginauthmethod

target = "http://192.168.2.131/dvwa/"
loginurl = "http://192.168.2.131/dvwa/login.php"
username = "1234"
password = "qwer"
contextregex = "\Qhttp://192.168.2.131/dvwa\E.*"
authmethod = loginauthmethod.HTTP_AUTHENTICATION
loggedinindicator = ".*This page is hidden.*"
loggedoutindicator = ".*Login failed.*"

zap = owaspzap()

zap.initialize(str(datetime.now()), target, contextregex)
zap.authenticate(loginurl, username, password, loggedinindicator, loggedoutindicator, authmethod)
zap.spider(target)
zap.passive_scan()
zap.active_scan(target)
print(zap.get_spider())
print(zap.get_alerts())


#print(str(zap))
zap.context_remove()