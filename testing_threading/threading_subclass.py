import threading
import logging

logging.basicConfig(level=logging.DEBUG,
					format='(%(threadName)s) %(message)s',
					)

class MyThread(threading.Thread):

	def run(self):
		logging.debug('running in run')
		return

for i in range(5):
	t = MyThread()
	t.start()