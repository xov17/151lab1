import random, socket, sys, time, hashlib
import logging
import threading
import time
from random import choice
from string import lowercase
from decimal import Decimal

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


logging.basicConfig(level=logging.DEBUG,
					format='%(asctime)s (%(threadName)-2s) %(message)s')

MAX = 65535
PORT = 1083
WINDOW_SIZE = 5
PACKET_SIZE = 64

RETURNED_PACKETS = 0
PACKET_LOSS = 0
DELAY = 0.001

START_TIME = 0
END_TIME = 0



CONNECTED_THREADS = 0
#	Test for different window sizes, same packet size

# 	Test for same window size, different packet sizes

def consumer_client(cond,e):
	global PACKET_LOSS
	global RETURNED_PACKETS
	global START_TIME
	global END_TIME
	global CONNECTED_THREADS
	logging.debug('Starting consumer thread')
	hostname = sys.argv[2]
	t = threading.currentThread()

	with cond:		
	   
		
		
		#message = "".join(choice(lowercase) for i in range(PACKET_SIZE))
		message = "a" * PACKET_SIZE

		try:
			s.connect((hostname, PORT))
	   		logging.debug('WAITING: Client socket name is %s', s.getsockname())
	   		CONNECTED_THREADS = CONNECTED_THREADS + 1
   		except: 
   			raise
	   	if (CONNECTED_THREADS == WINDOW_SIZE):
	   		logging.debug('Equal connected threads and window size')
	   		print "e.isSet() = ", e.isSet()
	   		e.set()
   		else:
   			print "e.isSet() = ", e.isSet()
   			print "entered not equal connected threads and window size"
		#while (started_threads != WINDOW_SIZE):
		#	logging.debug('stalling')
		if (e.isSet() != True):
			cond.wait()
		else:
			print "entered else for isset"
		s.send(message)
		logging.debug('Sent message: %s', message)
	


		print "AT SETTING DELAY"
		s.settimeout(DELAY)
		cond.acquire()

		try:
 			data = s.recv(MAX)
 			logging.debug('The server says: %s', data)
 			if (data == message):
 				cond.acquire()
 				RETURNED_PACKETS = RETURNED_PACKETS + 1
 				cond.release()
 			else:
 				cond.acquire()
 				PACKET_LOSS = PACKET_LOSS +1
 				cond.release()
 			
 		except socket.timeout: # DID NOT RECEIVE 
 		#	delay *= 2 #wait even longer for the next request
 		#	if delay > 2.0:
 		#		raise RuntimeError('I think the server is down')
 			logging.debug('Socket Timeout')
 			cond.acquire()
 			PACKET_LOSS = PACKET_LOSS + 1
 			logging.debug('Packet loss: %d', PACKET_LOSS)
 			cond.release()
 		except:
 			raise
 		cond.release()
		print "Alive threads: ", threading.enumerate()
		

		
  		#print 'Client socket name is', s.getsockname()

def producer_client(cond, e):
	global START_TIME
	logging.debug('Starting producer thread')
	with cond:
		logging.debug('Making resource available')
		
		cond.notifyAll()
		START_TIME = time.time()


if 2<= len(sys.argv) <= 3 and sys.argv[1] == 'server':
	interface = sys.argv[2] if len(sys.argv) > 2 else ''
	s.bind((interface, PORT))
	logging.debug('Listening at %s', s.getsockname() )


	wrong_msg = "Wrong Message"

	while True:
		data, address = s.recvfrom(MAX)
		logging.debug('Listening at %s', s.getsockname() )
		#print 'The client at', address, 'says:', repr(data)

		if (len(data) == PACKET_SIZE):
			logging.debug("Received correct length")
			s.sendto(data,address)
		else:
			logging.debug("Received wrong length")
			s.sendto(wrong_msg,address)



elif len(sys.argv) == 3 and sys.argv[1] == 'client':

	# Time interval after which result/s will be displayed
	# Results may be multiple as 

	interval = float(raw_input('Time interval (in sec.)? '))
	print "Interval: ", interval
	
	main_start = time.time()
	delta = 0
	
	main_lock = threading.RLock()
	threads = []

	e = threading.Event()

	while (delta < interval): 
		print "Alive threads: ", threading.enumerate()
		e.clear()
		CONNECTED_THREADS = 0
		RETURNED_PACKETS = 0
		PACKET_LOSS = 0

		del threads[:]

		condition = threading.Condition(main_lock)
		
		
		for i in range(WINDOW_SIZE):
			t = threading.Thread(target=consumer_client, args=(condition,e))
			threads.append(t)
			t.start()
		p = threading.Thread(name='p_client', target=producer_client, args=(condition,e))
		e.wait()
		p.start()

		print "HERE"
		for x in threads:
			x.join()
		logging.debug('Total Packet loss: %d', PACKET_LOSS)

		END_TIME = time.time()
		RTT = END_TIME-START_TIME
		print "Packet Size: ", PACKET_SIZE
		print "Window Size: ", WINDOW_SIZE
		print "Packet Loss: ", PACKET_LOSS
		print "RTT: ", RTT
		print "Returned Packets: ", RETURNED_PACKETS
		data_received = (RETURNED_PACKETS*PACKET_SIZE)
		throughput = data_received/(RTT/2)
		throughput_b = (8*data_received)/(RTT/2)
		throughput_kb = float((data_received/1024)/(RTT/2))

		throughput_mb = float((data_received/(1024*1024))/(RTT/2))
		print "Throughput: ", throughput_mb, " mb/sec"
		print "Throughput: ", throughput_kb, " kb/sec"
		print "Throughput: ", throughput, " bytes/sec"
		print "Throughput: ", throughput_b, " bits/sec"
		print "data bytes: ", data_received
		print "data kb: ", float(data_received/1024)
		print "data mb: ", float(data_received/(1024*1024))


		delta = END_TIME - main_start
		print END_TIME
		print main_start
		print "Delta: ", delta
	print "out of loop"

	
	
else:
	print >>sys.stderr, 'usage: udp_remote.py server [ <interface> ]'
	print >>sys.stderr, '   or: udp_remote.py client <host>'
	sys.exit(2)


