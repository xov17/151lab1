# CoE151: Lab 1
# (1) End-to-end (maximum) throughput
# (2) Round-Trip Time
# (3) Packet Loss
#
# Should display minimum, maximum and average values

# (1) End-to-end (maximum) throughput
#   
# (2) Round-Trip Time
# (3) Packet Loss

# How to Use:
# Server: python udp.py server HOST(optional)
#   ex: python udp.py server
# Client: python udp.py client HOST
#   ex: python udp.py 127.0.0.1

import random, socket, sys, time
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1060

if 2<= len(sys.argv) <= 3 and sys.argv[1] == 'server':
    interface = sys.argv[2] if len(sys.argv) > 2 else ''
    s.bind((interface, PORT))
    print 'Listening at', s.getsockname()
    while True:
        data, address = s.recvfrom(MAX)
        print 'The client at', address, 'says:', repr(data)
        if (data ==  'lhfhgklahglhairhiwah'): 
            print 'correct data'
            print 'Your data was %d bytes' % len(data)
            s.sendto(data,address)
        else:
            print 'wrong data'


     #   if random.randint(0,1):
     #       print 'The client at', address, 'says:', repr(data)
     #       s.sendto('Your data was %d bytes' % len(data), address)
     #   else:
     #       print 'Pretending to drop packet from', address

elif len(sys.argv) == 3 and sys.argv[1] == 'client':
    hostname = sys.argv[2]
    s.connect((hostname, PORT))
    print 'Client socket name is', s.getsockname()
    delay = 0.1
    while True:
        interval = raw_input('Time interval (in sec.)? ')
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
                s.send(example)

                # Assuming that UDP client doesn't apply delay while waiting for server
                try: 
                    data, address = s.recvfrom(MAX)
                except:
                    # Lost packet from Server to Client
                    raise #Real error   

                # Testing for loss
                print 'DEBUG:', data, address
                if(data == 'lhfhgklahglhairhiwah'):
                    print 'yes'
                    b = time.time()
                    delta_packet = b-a #Time since sending for each packet
                    print delta_packet
                else:
                    print 'no'
            
               # confirm = d[0]
               #server = d[1]

                #print 'Return Text: ' + confirm
            except socket.error:
                print 'Error.'
                sys.exit()

            delta = time.time() - start
            if delta >= abort_after:
                break
    count = str(count)
    print 'Msg count: ' + count


       
        
           # break # we are done, and can stop looping
        
   # print 'The server says', repr(data)
    
else:  
    print >>sys.stderr, 'usage: udp_remote.py server [ <interface> ]'
    print >>sys.stderr, '   or: udp_remote.py client <host>'
    sys.exit(2)
    
    
#   Metrics to Measure 
#   (1) Round - Trip Time
#   (2) 
        
        
        
        
        
    
    
    
    
