#!/bin/sh

# exec sudo sh install.sh

# --------------------------- root exec
if [ $USER != "root" -o $UID != 0 ]
then
  echo "need sudo !"
  exit 1
fi

sudo apt install python3 -y
sudo apt install python3-mysqldb -y


echo "
# edit crontab with  $ crontab -e

# Execut script all days at 3 o'clocks

# m h  dom mon dow   command
0 3 * * * /usr/bin/python3 /var/www/domotix-server/domotixServer.py
" 
