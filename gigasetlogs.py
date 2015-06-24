"""
	Program: 	Gigasetlogs
	Use:	 	read the logs of a gigaset router and save it to a log file.
	Author:		KoalaTea
"""
#incomplete more work to do


#attempting to do it with sockets as well another day
"""
import socket

request = b"GET / HTTP/1.1\nHOST: 192.168.254.254\n\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.254.254", 80))
s.send(request)
result = s.recv(10000)
while (len(result)>0):
        print(result)
        result = s.recv(10000)
"""
import sys,urllib.request,re
import os.path

#setting up and grabbing the data
J="http://192.168.254.254/syslogshow.htm"
A=urllib.request.urlopen(J)
AB=A.read()

#check if GigasetBackup exists
if os.path.exists('GigasetBackup.txt'):
    #read for the last line of the file
    file = open('GigasetBackup.txt', 'r')
    for line in file:
        lastentry = line
    file.close()

    #open backup and add to the end of backupfile any new entries
    file = open('GigasetBackup.txt', 'a')
    data=str(AB).split('<TR>')
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
            newentryj = newentry[2] + newentry[0] + newentry[1] + newentry[3]
            newentryj = newentryj + newentry[4] + newentry[5]
            lastentryj = lastentrysp[2] + lastentrysp[0] + lastentrysp[1]
            lastentryj = lastentryj + lastentrysp[3] + lastentrysp[4]
            lastentryj = lastentryj + lastentrysp[5]
            if int(newentryj) > int(lastentryj):
                new = 1
                file.write(entry.group(1) + '\n')
else:
    file = open('GigasetBackup.txt', 'w')
    data=str(AB).split('<TR>')
    new=0;
    for line in data:
        entry = re.search(r'<pre>(.*)</pre>',line,flags=0)
        if entry:
            file.write(entry.group(1) + '\n')
file.close()
