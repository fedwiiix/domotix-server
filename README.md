# Domotix Server
Back-end of domotix server in Aya Project

this backend allows to have an SMS notification for agenda event. It allows database saves.

### Use

Get Events in calendar and notify

### Install
 - sudo chmod 100 install.sh
 - sudo sh install.sh
 - complete init file with your database connection data
 - edit crontab with  $ crontab -e
 - add next text for execut script all days at 3 o'clocks

```
m h  dom mon dow   command
0 3 * * * /usr/bin/python3 /var/www/domotix-server/domotixServer.py
```

* need create mysql user with right to save databases:
  * SHOW DATABASES
  * LOCK TABLES 
