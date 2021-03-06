import random, socket, sys, time, hashlib
import logging
import threading
import time
from random import choice
from string import lowercase

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

logging.basicConfig(level=logging.CRITICAL,
					format='%(asctime)s (%(threadName)-2s) %(message)s')

MAX = 65535
PORT = 1073
WINDOW_SIZE = 10
PACKET_SIZE = 10

PACKET_LOSS = 0
DELAY = 0.001

START_TIME = 0
END_TIME = 0


RETURNED_PACKETS = 0



def consumer_client(cond):
	global PACKET_LOSS
	global RETURNED_PACKETS
	global START_TIME
	global END_TIME
	logging.debug('Starting consumer thread')
	hostname = sys.argv[2]
	t = threading.currentThread()
	with cond:		
	   	s.connect((hostname, PORT))
	   	logging.debug('WAITING: Client socket name is %s', s.getsockname())
		
		logging.debug('Resource is available to consumer')
		message = "".join(choice(lowercase) for i in range(PACKET_SIZE))
		cond.wait()
		s.send(message)
		logging.debug('Sent message: %s', message)
	

"""
	Client
		has timeout -> for receiving a loss packet
		checks if message received is same
			"wrong message"
			received message

"""
		s.settimeout(DELAY)
		try:
 			data = s.recv(MAX)
 			logging.debug('The server says: %s', data)
 			if (data == message):
 				RETURNED_PACKETS = RETURNED_PACKETS + 1
 			else:
 				PACKET_LOSS = PACKET_LOSS +1
 			
 		except socket.timeout: # DID NOT RECEIVE 
 		#	delay *= 2 #wait even longer for the next request
 		#	if delay > 2.0:
 		#		raise RuntimeError('I think the server is down')
 			logging.debug('Socket Timeout')
 			cond.acquire()
 			PACKET_LOSS = PACKET_LOSS + 1
 			logging.debug('Packet loss: %d', PACKET_LOSS)
 			cond.release()
		
"""
		except:
			logging.debug('Packet loss increments')
			cond.acquire()
			PACKET_LOSS = PACKET_LOSS + 1
			logging.debug('Packet loss: %d', PACKET_LOSS)
			#raise 
			cond.release()
"""		
		cond.acquire()
		if ((RETURNED_PACKETS+ PACKET_LOSS) == WINDOW_SIZE):
			logging.debug('Total Packet loss: %d', PACKET_LOSS)
			END_TIME = time.time()
			RTT = END_TIME-START_TIME
			print "Packet Size: ", PACKET_SIZE
			print "Window Size: ", WINDOW_SIZE
			print "Packet Loss: ", PACKET_LOSS
			print "RTT: ", RTT
			data_received = (RETURNED_PACKETS*PACKET_SIZE)
			throughput = data_received/RTT			
			throughput_b = (8*data_received)/RTT
			throughput_kb = (data_received/1024)/RTT

			throughput_mb = (data_received/(1024*1024))/RTT
			print "Throughput: ", throughput_mb, " mb/sec"
			print "Throughput: ", throughput_kb, " kb/sec"
			print "Throughput: ", throughput, " bytes/sec"
			print "Throughput: ", throughput_b, " bits/sec"
			print "data kb: ", data_received/1024
			print "data mb: ", data_received/(1024*1024)
			#logging.debug('RTT: %lf', END_TIME-START_TIME)
		cond.release()
  		#print 'Client socket name is', s.getsockname()

def producer_client(cond):
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
	condition = threading.Condition()

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
"""
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
"""
"""
	Client sends data to server.
	SYN_ACK

	#Server may or may not receive data
	if (Server receives data) {
		send data back to client
	} else {

	}

	Server
		checks length
			if wrong, sends error code to client "wrong message"

			if right, sends back message to client

	Client
		has timeout -> for receiving a loss packet
		checks if message received is same
			"wrong message"
			received message


"""



elif len(sys.argv) == 3 and sys.argv[1] == 'client':

	# Time interval after which result/s will be displayed
	# Results may be multiple as 
	interval = raw_input('Time interval (in sec.)? ')
	abort_after = float(interval)
"""
	Release results after interval

	Run test for interval, storing different results


"""

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


