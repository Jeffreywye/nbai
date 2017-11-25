#!env/bin/python
import datetime
import os
import time

server_updated_today = False

def do_server_update():
    os.popen("killall server.py").read()
    os.popen('./src/server.py').read()

def do_git_pull():
    os.chdir("/var/www/nbai_live")
    result = os.popen("git pull").read()

    if result != 'Already up-to-date.\n':
        do_server_update()
        
while(True):
    time_now = datetime.datetime.now()
    if time_now.hour == 1 and server_updated_today == False:
        do_server_update()
        server_updated_today = True
    if time_now.hour == 2 and server_updated_today == True:
        server_updated_today == False

    do_git_pull()
    time.sleep(20)
