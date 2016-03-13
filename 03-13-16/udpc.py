import random, socket, sys, time, hashlib
import logging
import threading
import time
from random import choice
from string import lowercase
from decimal import Decimal
import csv

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
	# TIME	WINDOW SIZE	PACKET SIZE	END-TO-END THROUGHPUT	ROUND-TRIP TIME	PACKET LOSS
	headers = ["TIMESTAMP","WINDOW SIZE", "PACKET SIZE", "END-TO-END THROUGHPUT (bytes/sec)", "END-TO-END THROUGHPUT (bits/sec)", "ROUND-TRIP TIME", "PACKET LOSS"]
	# 6 columns

	TIMESTAMP_LIST = []
	WINDOW_SIZE_LIST = []
	PACKET_SIZE_LIST = []
	THROUGHPUT_LIST = []
	THROUGHPUTB_LIST = []
	RTT_LIST = []
	PACKET_LOSS_LIST = []

	



	MAIN_LIST = []
	MAIN_LIST.append(headers)
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

		TIMESTAMP_LIST.append(END_TIME)
		WINDOW_SIZE_LIST.append(WINDOW_SIZE)
		PACKET_SIZE_LIST.append(PACKET_SIZE)
		THROUGHPUT_LIST.append(throughput)
		THROUGHPUTB_LIST.append(throughput_b)
		RTT_LIST.append(RTT)
		PACKET_LOSS_LIST.append(PACKET_LOSS)

		MAIN_LIST.append([END_TIME, WINDOW_SIZE, PACKET_SIZE,throughput, throughput_b, RTT, PACKET_LOSS ])

		delta = END_TIME - main_start
		print END_TIME
		print main_start
		print "Delta: ", delta
	print "out of loop"
	
	print "============ MAXIMUM VALUES ============"
	max_value = max(RTT_LIST)
	max_index = RTT_LIST.index(max_value)
	print "Max RTT: ", max_value
	print "		-> TIMESTAMP: ", TIMESTAMP_LIST[max_index]
	print "		-> WINDOW SIZE: ",WINDOW_SIZE_LIST[max_index]
	print "		-> PACKET SIZE: ", PACKET_SIZE_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bytes/sec): ", THROUGHPUT_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bits/sec): ", THROUGHPUTB_LIST[max_index]
	print "		-> RTT: ", RTT_LIST[max_index]
	print "		-> PACKET LOSS ", PACKET_LOSS_LIST[max_index]

	max_value = max(THROUGHPUTB_LIST)
	max_index = THROUGHPUTB_LIST.index(max_value)
	print "Max Throughput: ", max_value
	print "		-> TIMESTAMP: ", TIMESTAMP_LIST[max_index]
	print "		-> WINDOW SIZE: ",WINDOW_SIZE_LIST[max_index]
	print "		-> PACKET SIZE: ", PACKET_SIZE_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bytes/sec): ", THROUGHPUT_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bits/sec): ", THROUGHPUTB_LIST[max_index]
	print "		-> RTT: ", RTT_LIST[max_index]
	print "		-> PACKET LOSS ", PACKET_LOSS_LIST[max_index]
	max_value = max(PACKET_LOSS_LIST)
	max_index = PACKET_LOSS_LIST.index(max_value)
	print "Max Packet Loss: ", max_value
	print "		-> TIMESTAMP: ", TIMESTAMP_LIST[max_index]
	print "		-> WINDOW SIZE: ",WINDOW_SIZE_LIST[max_index]
	print "		-> PACKET SIZE: ", PACKET_SIZE_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bytes/sec): ", THROUGHPUT_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bits/sec): ", THROUGHPUTB_LIST[max_index]
	print "		-> RTT: ", RTT_LIST[max_index]
	print "		-> PACKET LOSS ", PACKET_LOSS_LIST[max_index]

	print " "

	print "============ MINIMUM VALUES ============"
	max_value = min(RTT_LIST)
	max_index = RTT_LIST.index(max_value)
	print "Min RTT: ", max_value
	print "		-> TIMESTAMP: ", TIMESTAMP_LIST[max_index]
	print "		-> WINDOW SIZE: ",WINDOW_SIZE_LIST[max_index]
	print "		-> PACKET SIZE: ",PACKET_SIZE_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bytes/sec): ", THROUGHPUT_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bits/sec): ", THROUGHPUTB_LIST[max_index]
	print "		-> RTT: ", RTT_LIST[max_index]
	print "		-> PACKET LOSS ", PACKET_LOSS_LIST[max_index]

	max_value = min(THROUGHPUTB_LIST)
	max_index = THROUGHPUTB_LIST.index(max_value)
	print "Min Throughput: ", max_value
	print "		-> TIMESTAMP: ", TIMESTAMP_LIST[max_index]
	print "		-> WINDOW SIZE: ",WINDOW_SIZE_LIST[max_index]
	print "		-> PACKET SIZE: ", PACKET_SIZE_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bytes/sec): ", THROUGHPUT_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bits/sec): ", THROUGHPUTB_LIST[max_index]
	print "		-> RTT: ", RTT_LIST[max_index]
	print "		-> PACKET LOSS ", PACKET_LOSS_LIST[max_index]
	max_value = min(PACKET_LOSS_LIST)
	max_index = PACKET_LOSS_LIST.index(max_value)
	print "Min Packet Loss: ", max_value
	print "		-> TIMESTAMP: ", TIMESTAMP_LIST[max_index]
	print "		-> WINDOW SIZE: ",WINDOW_SIZE_LIST[max_index]
	print "		-> PACKET SIZE: ", PACKET_SIZE_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bytes/sec): ", THROUGHPUT_LIST[max_index]
	print "		-> END-TO-END THROUGHPUT (bits/sec): ", THROUGHPUTB_LIST[max_index]
	print "		-> RTT: ", RTT_LIST[max_index]
	print "		-> PACKET LOSS ", PACKET_LOSS_LIST[max_index]

	print " "

	print "============ AVERAGE VALUES ============"
	print "Ave RTT: ", float(sum(RTT_LIST)/len(RTT_LIST))
	print "Ave Throughput (bits/sec): ", float(sum(THROUGHPUTB_LIST)/len(THROUGHPUTB_LIST))
	print "Ave Throughput (bytes/sec): ", float(sum(THROUGHPUT_LIST)/len(THROUGHPUT_LIST))
	print "Ave Packet Loss: ", float(sum(PACKET_LOSS_LIST)/len(PACKET_LOSS_LIST))


    
	
	with open("output.csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(MAIN_LIST)
	    

	
	
else:
	print >>sys.stderr, 'usage: udp_remote.py server [ <interface> ]'
	print >>sys.stderr, '   or: udp_remote.py client <host>'
	sys.exit(2)


