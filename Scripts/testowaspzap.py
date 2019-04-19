from datetime import datetime
from owaspzap import owaspzap
from loginauthmethod import loginauthmethod

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