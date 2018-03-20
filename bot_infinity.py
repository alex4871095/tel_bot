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

INTERVAL = 600
torrent_file = '/dev/tmp/Suicide.Squad.2016.WEB-DL.1080p.ExKinoRay.mkv'
transmission ='/usr/bin/transmission-cli -w /dev/tmp http://ru-free-tor.org/download/534342'
channel = random.randint(1,16)
channel = str(channel)
ffmpeg = '/usr/bin/ffmpeg -dn -i udp://@233.3.2.'+channel+':5000 -f null 111'

def inf_loop():
	global host
	global obj_t
	global obj_f
		host = subprocess.check_output("hostname",shell=True)
		host = host[:-1]
		print "hostname:", host
		message = 'doc406 doc407 doc408 doc409 doc410 doc411 doc412 doc413 doc414 doc415 doc416 doc417 doc418 doc419 doc420 doc421 doc422 doc423 doc424 doc425'
		arr = message.splitlines()
	        for item in arr:
                	if item.find(host) != -1:
                        	stop_proc("ffmpeg", "")
                                stop_proc("transmission", torrent_file)
                                obj_t = start_proc("transmission")
                                obj_f = start_proc("ffmpeg")
	return True

def start_proc(proc):
        if proc == "transmission":
                args = shlex.split(transmission)
                obj = subprocess.Popen(args)
        if proc == "ffmpeg":
                args = shlex.split(ffmpeg)
                obj = subprocess.Popen(args)
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
	if file_id != '':
		if os.access(file_id, os.W_OK):
			os.remove(file_id)
			tor_file = os.listdir('/root/.config/transmission/torrents/')
			os.remove("/root/.config/transmission/torrents/"+tor_file[0]+"")
                        tor_file = os.listdir('/root/.config/transmission/resume/')
                        os.remove("/root/.config/transmission/resume/"+tor_file[0]+"")
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
		inf_loop()
		time.sleep(INTERVAL)
	except KeyboardInterrupt:
		print 'Interupted by user..'
		break
