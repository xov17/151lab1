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
PORT = 1065
WINDOW_SIZE = 10
PACKET_SIZE = 1

"""
    s.bind((interface, PORT))
    print 'Listening at', s.getsockname()
"""
"""
def consumer_server(cond):	
	s.bind((interface, PORT))
	logging.debug('Listening at %s', s.getsockname() )
	#print 'Listening at', s.getsockname()
	#wait for the condition to start all servers
	# t = threading.currentThread()
	with cond:
		cond.wait()
		logging.debug('Will now receive at %s', s.getsockname() )
		#print "Now listening", s.getsockname(), 
		while True:
			data, address = s.recvfrom(MAX)
			logging.debug('The client at %s says: %s', address, repr(data))
			#print 'The client at', address, 'says:', repr(data)
			if (data ==  'lhfhgklahglhairhiwah'):
				logging.debug('Correct data')
				logging.debug('Your data was %d bytes', len(data))
				#print 'correct data'
				#print 'Your data was %d bytes' % len(data)
				s.sendto(data,address)
			else:
				logging.debug('Wrong data')
				#print 'wrong data'

def producer_server(cond):
	#set up the resource to be used by the consumer
	logging.debug('Starting producer thread')
	with cond:
		logging.debug('Making resource available')	
		cond.notifyAll()
"""

def consumer_client(cond):
	logging.debug('Starting consumer thread')
	hostname = sys.argv[2]
	t = threading.currentThread()
	with cond:
		logging.debug('Resource is available to consumer')
	   	s.connect((hostname, PORT))
	   	logging.debug('WAITING: Client socket name is %s', s.getsockname())
		cond.wait()
		message = "My message"
		s.send(message)
		logging.debug('Sent message: %s', message)
		while True:
			try:
	 			data = s.recv(MAX)
	 			logging.debug('The server says: %s', data)
	 		except socket.timeout:
	 			delay *= 2 #wait even longer for the next request
	 			if delay > 2.0:
	 				raise RuntimeError('I think the server is down')
			except:
				raise 
	
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
	while True:
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
			#print 'wrong data'
	"""
	condition = threading.Condition()
	for i in range(WINDOW_SIZE):
		t = threading.Thread(target=consumer_server, args=(condition,))	
		t.start()
	p = threading.Thread(name='p_server', target=producer_server, args=(condition,))
	p.start()
	"""


elif len(sys.argv) == 3 and sys.argv[1] == 'client':
	condition = threading.Condition()
	for i in range(WINDOW_SIZE):
		t = threading.Thread(target=consumer_client, args=(condition,))
		t.start()
	p = threading.Thread(name='p_client', target=producer_client, args=(condition,))
	p.start()
	
	
else:
	print >>sys.stderr, 'usage: udp_remote.py server [ <interface> ]'
	print >>sys.stderr, '   or: udp_remote.py client <host>'
	sys.exit(2)

