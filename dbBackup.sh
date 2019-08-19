#!/bin/bash

if [ -z $1 ]
then
	read -p 'user: ' -t 6 -s user # timeout 6sec et mdp
	echo $user
else
	user=$1
fi

if [ -z $2 ]
then
	read -p 'password: ' -t 6 -s pass
	echo "" 
else
	pass=$2
fi

echo "databases backed up"
# list of databases backed up
array=( domotix )


for i in "${array[@]}"
do
	echo $i
	mysqldump --user=$user --password=$pass $i > /var/www/domotix-server/dbBackup/$i-$(date +%F).sql
done

sleep 3
cd /var/www/domotix-server/dbBackup
tar zcvf dbBackup-$(date +%F).tar.gz domotix-$(date +%F).sql
if [ $? == '0' ]
then
	rm domotix-$(date +%F).sql
fi



