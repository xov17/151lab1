import socket
import sys
import time

HOST = ''
PORT = 8888

#Create Socket:

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Socket Created.'
except socket.error:
	print 'Socket Creation Failed.'
	sys.exit()

#Bind Socket to Local Host and Port

try:
	s.bind((HOST,PORT))
	print 'Bind Complete.'
except socket.error:
	print 'Binding Failed.'
	sys.exit()

#Server will keep communicating with the client:

while 1:
	d = s.recvfrom(1024)
	text = d[0]
	client = d[1]

	#if not text:
	#	break

	#print 'Text: ' + text
	if(d[0] == 'lhfhgklahglhairhiwah'):
		print 'yes'
		s.sendto(text, client)
	else:
		print 'no'

s.close()