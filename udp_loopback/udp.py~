#UDP Client and Server

import socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX= 65535
PORT = 1060
HOST = '127.0.0.1'
#HOST = '192.168.200.31'

if sys.argv[1:]==['server']:
    s.bind((HOST,PORT))
    print 'Listening at', s.getsockname()
    while True:
        data, address = s.recvfrom(MAX)
        print 'The client at', address, 'says', repr(data)
        s.sendto('Your data was %d bytes' % len(data), address)
        
elif sys.argv[1:] == ['client']:
    print 'Address before sending:', s.getsockname()
    s.sendto('This is my message', (HOST,PORT))
    print 'Address after sending', s.getsockname()
    data,address = s.recvfrom(MAX) #over promiscuous - see text!
    print 'The server', address, 'says', repr(data)
    
else:
    print >> sys.stderr, 'usage: udp.py server|client'
