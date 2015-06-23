"""
	Program: 	Gigasetlogs
	Use:	 	read the logs of a gigaset router and save it to a log file.
	Author:		KoalaTea
"""
#incomplete more work to do


#attempting to do it with sockets as well
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

    #open backup and add to the end any new entries
    #currently only works if new copy of the logs has the last line of old
    #logs still on there
    file = open('GigasetBackup.txt', 'a')
    data=str(AB).split('<TR>')
    new=0;
    for line in data:
        entry = re.search(r'<pre>(.*)</pre>',line,flags=0)
        if entry and new == 1:
            file.write(entry.group(1) + '\n')
        elif entry:
            if entry.group(1) == lastentry[0:-1]:
                new = 1
        #file.write(line + '\n')
else:
    file = open('GigasetBackup.txt', 'w')
    data=str(AB).split('<TR>')
    new=0;
    for line in data:
        entry = re.search(r'<pre>(.*)</pre>',line,flags=0)
        if entry:
            file.write(entry.group(1) + '\n')
file.close()
