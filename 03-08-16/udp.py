import random, socket, sys, time, hashlib
import logging
import threading
import time
from random import choice
from string import lowercase

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

logging.basicConfig(level=logging.DEBUG,
					format='%(asctime)s (%(threadName)-2s) %(message)s')

MAX = 65535
PORT = 1069
WINDOW_SIZE = 10
PACKET_SIZE = 10
#PACKET_LOSS = 0
DELAY = 0.1


def consumer_client(cond,cond2):
	
	logging.debug('Starting consumer thread')
	hostname = sys.argv[2]
	t = threading.currentThread()
	with cond:		
	   	s.connect((hostname, PORT))
	   	logging.debug('WAITING: Client socket name is %s', s.getsockname())
		cond.wait()
		logging.debug('Resource is available to consumer')
		message = "".join(choice(lowercase) for i in range(PACKET_SIZE))
		s.send(message)
		logging.debug('Sent message: %s', message)
		#while True:
		s.settimeout(DELAY)
		try:
 			data = s.recv(MAX)
 			logging.debug('The server says: %s', data)
 		except socket.timeout:
 		#	delay *= 2 #wait even longer for the next request
 		#	if delay > 2.0:
 		#		raise RuntimeError('I think the server is down')
 			logging.debug('Socket Timeout')
 			PL.increment()
 			PL.printLoss()
 			#PACKET_LOSS = PACKET_LOSS + 1
 			#logging.debug('Packet loss: %d', PACKET_LOSS)
		except:
			logging.debug('Packet loss increments')
			PL.increment()
 			PL.printLoss()
			#PACKET_LOSS = PACKET_LOSS + 1
			#logging.debug('Packet loss: %d', PACKET_LOSS)
			#raise 
	
  		#print 'Client socket name is', s.getsockname()

def producer_client(cond):
	logging.debug('Starting producer thread')
	with cond:
		logging.debug('Making resource available')
		cond.notifyAll()


if 2<= len(sys.argv) <= 3 and sys.argv[1] == 'server':
	interface = sys.argv[2] if len(sys.argv) > 2 else ''
	s.bind((interface, PORT))
	logging.debug('Listening at %s', s.getsockname() )

	PL = packetLoss()
	PL.printLoss()
	#while True:
	for x in range(WINDOW_SIZE-1):
		data, address = s.recvfrom(MAX)
		logging.debug('Listening at %s', s.getsockname() )
		#print 'The client at', address, 'says:', repr(data)
		if (data ==  'lhfhgklahglhairhiwah'): 
			print 'correct data'
			print 'Your data was %d bytes' % len(data)
			s.sendto(data,address)
		else:
			logging.debug('Data: %s , Your data was %d bytes', data, len(data))
			server_msg = "OK: "+ data
			s.sendto(server_msg,address)
			logging.debug('Data: %s , Address: %s', data, address)
			#print 'wrong data'\

	#logging.debug('ENDED, Packet loss: %d', PACKET_LOSS)



elif len(sys.argv) == 3 and sys.argv[1] == 'client':
	condition = threading.Condition()
	cond2 = threading.Condition()
	for i in range(WINDOW_SIZE):
		t = threading.Thread(target=consumer_client, args=(condition,cond2,))
		t.start()
	p = threading.Thread(name='p_client', target=producer_client, args=(condition,))
	p.start()
	cond2.wait()
	print "Cond2 finished waiting"
	
	
else:
	print >>sys.stderr, 'usage: udp_remote.py server [ <interface> ]'
	print >>sys.stderr, '   or: udp_remote.py client <host>'
	sys.exit(2)

