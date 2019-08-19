#! /usr/bin/python3
# -*- coding: utf-8 -*-
 
import os, time, datetime		
import MySQLdb   
import urllib.request, urllib.parse
import configparser

directory= os.path.dirname(__file__)
log_file = directory+'/domotixServer.log'
config_file = directory+'/config.ini'

Config = configparser.ConfigParser()				# get user and pass
Config.read(config_file)

dbhost = Config["Global"]['host']									# variable base de donnee
dbuser = Config["Global"]['user']
dbmdp = Config["Global"]['mdp']
dbbase = Config["Global"]['base']

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
nbError=0
def set_log(text):

	now = date = time.strftime('%H:%M %d-%m-%Y', time.localtime())
	file = open(log_file,'a') 
	file.write(now +" -> "+  text+'<br>\n') 
	print(now +" -> "+ text)
	file.close() 

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 

prec_heure=""
lien_sms=""

db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbmdp, db=dbbase) # on se connecte
cursor=db.cursor()
cursor.execute("""SELECT * FROM parametres""")		# on cherche les donnees d'envoie sms ou mail
parametres = cursor.fetchall()

for row in parametres:
	if row[0]=='lien_sms':
		lien_sms = str(row[1])
		if lien_sms !="":
			now = time.strftime('%d-%m %H:%M ', time.localtime())
			#urllib.request.urlopen(lien_sms + urllib.parse.quote_plus(now +"Démarage du serveur domotix"))
		else:
			set_log("Aucun lien sms disponible pour envoyer des notifications")

db.commit()
cursor.close()


def html_escape(text):
	return text.replace("&amp;", "&").replace( "&quot;",'"').replace( "&lt;","<").replace("&gt;",">").replace("&eacute;", "é").replace("&egrave;", "è").replace("&agrave;", "à").replace("&ccedil;", "ç").replace("&acirc;", "â").replace("&ecirc;", "ê").replace("&yuml;", "ÿ").replace("&iuml;", "ï")

while 1:

	try:		
		set_log("-----------------------------------------------------")
		set_log("check des évenements de la journée")
		
		cursor=db.cursor()

		cursor.execute("""SELECT * FROM `agenda` where date_event=DATE_FORMAT(NOW(), '%Y/%m/%d') or (MONTH(date_event)=MONTH(NOW()) and DAY(date_event)=DAY(NOW()) and recurence=1)""")		# on regarde si il y a des events today
		agendas = cursor.fetchall()

		jour_now = str(time.strftime('%e', time.localtime()))
		mois_now = str(time.strftime('%m', time.localtime()))
		cursor.execute("""SELECT * FROM `agenda_saint` WHERE saint_mois=MONTH(CURDATE()) and saint_jour=DAY(CURDATE())""")	
		agenda_saints = cursor.fetchall()
		db.commit()
		cursor.close()

		sms=""

		for row in agenda_saints:

			set_log("Aujourd'hui, fete de "+row[3])
			if str(row[5])=='1':
				sms+="Fete aujourd\'hui de : "+row[3]
				if row[4]:
					sms+=" et de "+row[4]
		
		date_now = time.strftime('%Y-%m-%d', time.localtime())

		for row in agendas:

			type_agenda= str(row[1])
			heure_event= str(row[3])
			event= str(row[5])
			rappel_event= row[8]
			type_rappel= row[9]
							
			if rappel_event == "Oui" or type_agenda =="Anniversaire":											# si demande de rapelle par sms

				if type_agenda =="Agenda":
					sms += "\nEvenement: "
				else:
					sms += "\nAnniversaire: "

				if type_rappel == "SMS":
					try:
						if heure_event == "0:00:00":
							set_log ("event: "+ html_escape(event))
							sms += html_escape(event)
						else:
							set_log ("event: "+html_escape(event)+" a "+heure_event)
							sms += html_escape(event)+" a "+heure_event
					except:
						set_log ("impossible d\'envoyer un sms")
		
		if sms != '' and lien_sms !="":
			urllib.request.urlopen(lien_sms + urllib.parse.quote_plus(sms))

		if datetime.datetime.today().weekday() == 1:	# save every monday
			os.system(directory+'/dbBackup.sh '+dbuser+' '+dbmdp)
			set_log ("save database")

	except:
		set_log ('Error sur le serveur')
		urllib.request.urlopen(lien_sms + urllib.parse.quote_plus("le back end s'est arrêté"))

		nbError+=1
		time.sleep(1)

		if nbError == 5:
			exit(0)

	break
			
