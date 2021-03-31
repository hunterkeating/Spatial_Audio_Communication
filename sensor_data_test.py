# This code will allow you to see the data being sent from the android app 
import socket, traceback

host = ''
port = 5556 # This port should match the port you are sending data to on the phone

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

while 1:
    try:
        message, address = s.recvfrom(8192)
        y = message.decode("utf-8") # Standard encoding for characters. y holds useful data
        print(y)
        
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
