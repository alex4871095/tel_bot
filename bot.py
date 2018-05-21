#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import os
import subprocess
import re
import random
import shlex
import signal
import random

#requests.packages.urllib3.disable_warnings()
INTERVAL = 5  
ADMIN_ID = 111111111
URL = 'https://api.telegram.org/bot' 
TOKEN = 'XXX:YYY'
offset = 0
torrent_file = '/dev/tmp/movie.mkv'
speedtest = 'speedtest'
transmission ='/usr/bin/transmission-cli -w /dev/tmp http://ru-free-tor.org/download/534342'
channel = random.randint(1,16)
channel = str(channel)
ffmpeg = '/usr/bin/ffmpeg -dn -i udp://@233.3.2.'+channel+':5000 -f null 111'

def make_url_query_string(params):
		return '?' + '&'.join([str(key) + '=' + str(params[key]) for key in params])

def check_updates(limit=5):
	global offset
	global host
	global obj_t
	global obj_f
	params = make_url_query_string({'offset': offset+1, 'limit': limit, 'timeout': 0})
	request = requests.get(URL + TOKEN + '/getUpdates' + params)
	if not request.status_code == 200: return False
	if not request.json()['ok']: return False
	if not request.json()['result']: return False
	for update in request.json()['result']:
		if update.has_key("edited_message") == True:
			print "Edited message"
			continue
		offset = update['update_id']
		from_id = update['message']['from']['id']
		if (from_id != ADMIN_ID):
			send_respond("You're not autorized to use me!", from_id)
			print "Rogue access from:", from_id
			continue
		message = update['message']['text']
		print '>> OFFSET: ', offset
		print '>> MESSAGE:', message
		print '-' * 10
		host = subprocess.check_output("hostname",shell=True)
		host = host[:-1]
		print "hostname:", host
		arr = message.splitlines()
	        for item in arr:
			if item.find('hello') != -1:
				send_respond("Host "+host+" is here, Boss. Waiting for commands..", from_id)

			if item.find('start') !=-1:
	                	if item.find(host) != -1:
					send_respond("host "+host+" is waking up..", ADMIN_ID)
					start_proc("speedtest")
					obj_t = start_proc("transmission")
					obj_f = start_proc("ffmpeg")

                        if item.find('stop') !=-1:
	                 	if item.find(host) != -1:
					stop_proc("ffmpeg", "")
					stop_proc("transmission", torrent_file)

                        if item.find('reload') !=-1:
                                if item.find(host) != -1:
                                        stop_proc("ffmpeg", "")
                                        stop_proc("transmission", torrent_file)
                                        start_proc("speedtest")
                                        obj_t = start_proc("transmission")
                                        obj_f = start_proc("ffmpeg")

def send_respond(text, chat_id):

	params = make_url_query_string({'chat_id': chat_id, 'text': text})
	request = requests.get(URL + TOKEN + '/sendMessage' + params)
	if not request.status_code == 200: return False
	if not request.json()['ok']: return False
	return True

def start_proc(proc):

	if proc == "speedtest":
		res=subprocess.check_output("speedtest",shell=True)
		send_respond(res, ADMIN_ID)
		obj = 0
#	else:
#		send_respond("host "+host+" is starting "+proc+"", ADMIN_ID)
#		args = shlex.split(proc)
#		obj = subprocess.Popen(args)
#		if obj !=0:
#			send_respond(""+proc+" is started on host "+host+"", ADMIN_ID)
        if proc == "transmission":
		send_respond("host "+host+" is starting transmission", ADMIN_ID)
                args = shlex.split(transmission)
                obj = subprocess.Popen(args)
                if obj !=0:
                        send_respond("transmission is started on host "+host+"", ADMIN_ID)
        if proc == "ffmpeg":
                send_respond("host "+host+" is starting ffmpeg", ADMIN_ID)
                args = shlex.split(ffmpeg)
                obj = subprocess.Popen(args)
                if obj !=0:
                        send_respond("ffmpeg is started on host "+host+"", ADMIN_ID)
	return obj

def stop_proc(proc, file_id):
	pid = os.system("pgrep "+proc+"")
	if pid !=256:
		if proc == "transmission":
			obj_t.terminate()
			obj_t.communicate()
		if proc == "ffmpeg":
                        obj_f.terminate()
                        obj_f.communicate()
		send_respond(""+proc+" is stopped on host "+host+"", ADMIN_ID)
	if file_id != '':
		if os.access(file_id, os.W_OK):
			os.remove(file_id)
			tor_file = os.listdir('/root/.config/transmission/torrents/')
			os.remove("/root/.config/transmission/torrents/"+tor_file[0]+"")
                        tor_file = os.listdir('/root/.config/transmission/resume/')
                        os.remove("/root/.config/transmission/resume/"+tor_file[0]+"")
			send_respond("torrent file "+file_id+" is removed on host "+host+"", ADMIN_ID)
	return True


if not __name__ == "__main__": exit()
while (subprocess.check_output("ip rou", shell=True) == ""):
	time.sleep(4)
	print "Sleeping"

time.sleep(5)
os.system("echo nameserver 8.8.8.8 > /etc/resolv.conf")
os.system("mkdir /dev/tmp")

while True:
	try:
		check_updates()
		time.sleep(INTERVAL)
	except KeyboardInterrupt:
		print 'Interupted by user..'
		break
