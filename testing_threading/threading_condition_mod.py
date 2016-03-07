import logging
import threading
import time
from random import choice
from string import lowercase

logging.basicConfig(level=logging.DEBUG,
					format='%(asctime)s (%(threadName)-2s) %(message)s')

def consumer(cond, packetSize):
	"""wait for the condition and use the resource"""
	logging.debug('Starting consumer thread')
	#string_val = "x" * packetSize
	string_val = "".join(choice(lowercase) for i in range(packetSize))
	t = threading.currentThread()
	with cond:
		cond.wait()
		logging.debug('Resource is available to consumer')
		print string_val

def producer(cond):
	"""set up the resource to be used by the consumer"""
	logging.debug('Starting producer thread')
	with cond:
		logging.debug('Making resource available')
		cond.notifyAll()

packetSize = 60
condition = threading.Condition()
c1 = threading.Thread(name='c1', target=consumer, args=(condition,packetSize))
c2 = threading.Thread(name='c2', target=consumer, args=(condition,packetSize))
p = threading.Thread(name='p', target=producer, args=(condition,))

c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()