import socket
import sys
import time
import datetime

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
	print 'Socket Creation Failed'
	sys.exit()

HOST = '' #10.51.78.254
PORT = 8888



while 1:
	interval = raw_input('Time interval? ')

	#abort_after = int(interval)
	abort_after = float(interval)
	start = time.time()

	example = 'lhfhgklahglhairhiwah'

	count = 0
	delta = 0

	print 'Sending...'

	while delta <= abort_after:
		count = count + 1
		try:
			a = time.time()
			s.sendto(example, (HOST,PORT))
			d = s.recvfrom(1024)
			if(d[0] == 'lhfhgklahglhairhiwah'):
				print 'yes'
				b = time.time()
				delta = b-a
				print delta
			else:
				print 'no'
		
			confirm = d[0]
			server = d[1]

			#print 'Return Text: ' + confirm
		except socket.error:
			print 'Error.'
			sys.exit()

		delta = time.time() - start
		if delta >= abort_after:
			break

	count = str(count)
	print 'Msg count: ' + count