"""
	Program: 	Gigasetlogs2
	Use:	 	read the logs of a gigaset router and save it to log
                        file, using sockets instead of urllib to connect.
	Author:		KoalaTea
"""


import socket
import os.path
import re
from apscheduler.schedulers.blocking import BlockingScheduler

#setup
request = b"GET /syslogshow.htm HTTP/1.1\r\n\r\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scheduler = BlockingScheduler()

def Backup():
    #gathering new data every call
    s.connect(("192.168.254.254", 80))
    s.send(request)
    result = s.recv(10000)
    string = '' #AB in gigasetlogs.py
    while result:
        string = string + str(result)
        result = s.recv(10000)
    s.close()
    
    #check if GigasetBackup exists
    if os.path.exists('GigasetBackup.txt'):
        #read for the last line of the file
        file = open('GigasetBackup.txt', 'r')
        for line in file:
            lastentry = line
        file.close()

        #open backup and add to the end of backupfile any new entries
        file = open('GigasetBackup.txt', 'a')
        data=string.split('<TR>')
        new=0;
        for line in data:
            entry = re.search(r'<pre>(.*)</pre>',line,flags=0)
            if entry and new == 1:
                file.write(entry.group(1) + '\n')
            elif entry:
                newentry = re.split('/|:|\s',entry.group(1))
                lastentrysp = re.split('/|:|\s', lastentry)
            
                #checking dates for newer entry by concat yearmonthdayhourminsec
                #and then comparing
                #because of the difference from gigasetlogs.py newentry[0]
                #sometimes has a 'b'.... no idea why workaround in the code
                if len(newentry[0]) > 2:
                    new = re.search(r'\D*(\d*)\D*',newentry[1],flags=0)
                    newentry[1] = new.group(1)
                    newentryj = newentry[2] + newentry[0] + newentry[1]
                    newentryj = newentryj + newentry[3] + newentry[4]
                    newentryj = newentryj + newentry[5]
                else:
                    newentryj = newentry[2] + newentry[0] + newentry[1]
                    newentryj = newentryj + newentry[3] + newentry[4]
                    newentryj = newentryj + newentry[5]
                lastentryj = lastentrysp[2] + lastentrysp[0] + lastentrysp[1]
                lastentryj = lastentryj + lastentrysp[3] + lastentrysp[4]
                lastentryj = lastentryj + lastentrysp[5]
                if int(newentryj) > int(lastentryj):
                    new = 1
                    file.write(entry.group(1) + '\n')
    else:
        file = open('GigasetBackup.txt', 'w')
        data=string.split('<TR>')
        new=0;
        for line in data:
            entry = re.search(r'<pre>(.*)</pre>',line,flags=0)
            if entry:
                file.write(entry.group(1) + '\n')
    file.close()


#run once before starting the scheduler
Backup()
scheduler.add_job(Backup, 'interval', hours=1)
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    raise



