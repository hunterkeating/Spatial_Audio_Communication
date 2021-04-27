import socket, traceback
from math import sin, cos, sqrt, atan2, radians, pi, atan, degrees
import OSC_server, map_function

final_angle = None

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
TARGET_PORT = 5555 #Port that you are sending data to on other processor
TARGET_IP = "192.168.16.177" # IP address of other processor
HOST_PORT1  = 5556 #Port receiving data from phone
HOST_PORT2 = 5557 #Port receiving data from other processor

# For data from the phone
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock1.bind((HOST, HOST_PORT1))

# For GPS coords from other computer
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind((HOST, HOST_PORT2))

# For sending data to other computers
sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        message, address = sock1.recvfrom(8192) 
        y = message.decode("utf-8") # Standard encoding for characters. y holds useful data
        keyword = ','
        before_keyword, keyword, after_keyword = y.partition(keyword)
        before_keyword, keyword, after_keyword = after_keyword.partition(keyword)
        before_keyword, keyword, after_keyword = after_keyword.partition(keyword)
        thislati = after_keyword[0:9]
        before_keyword, keyword, after_keyword = after_keyword.partition(keyword)
        thislong = after_keyword[0:9]
            
        #print('This latitude:', thislati)
        #print('This longitude:', thislong)
            
            
        #Send coordinates to other laptop
        #print("Sending GPS...")
        space = " "
        coords_to_send = space.join((thislati, thislong)) # To make sent string as "lat long"
        sock3.sendto(coords_to_send.encode("UTF-8"), (TARGET_IP, TARGET_PORT))
        #print("Sent %s to %s at %d" % (coords_to_send, TARGET_IP, TARGET_PORT))
            
        # Receive coordinates from other laptop
        #print("Receiving GPS...")
        received_coords, addr = sock2.recvfrom(4096)
        received_coords = received_coords.decode("utf-8")
        #print("Received: %s" % received_coords)
            
        if received_coords[0] == '-':
            otherlati = received_coords[0:10]
        else:
            otherlati = received_coords[0:9]
        if received_coords[10] == '-':
            otherlong = received_coords[10:20]
        else:
            otherlong = received_coords[10:19]
        #print('Other latitude:', otherlati)
        #print('Other longitude:', otherlong)



            

        orientation = y[0:5]
                
        #print('Orientation:', orientation)

        orientation = float(orientation) # Because all in string form when entered
        otherlat = float(otherlati)
        otherlon = float(otherlong)
        thislat =float(thislati)
        thislon = float(thislong)
        thislatr = radians(thislat)
        thislonr = radians(thislon)
        otherlatr = radians(otherlat)
        otherlonr = radians(otherlon)
        dlat=otherlatr-thislatr # Difference in between the 2 nodes latitude
        dlon=otherlonr-thislonr # Difference in between the 2 nodes longitude

        # Determining which quadrant other lat long is with respect to this lat long
        if otherlatr==thislatr and otherlonr==thislonr:
            result=0 # Assigns angle between this location and other location clockwise from true north
        elif otherlonr>thislonr:
            if otherlatr==thislatr:
                result=(pi/2) # Assigns angle between this location and other location clockwise from true north
            elif otherlatr>thislatr:
                result=atan(abs(dlon)/abs(dlat)) # Assigns angle between this location and other location clockwise from true north
            elif otherlatr<thislatr:
                result=(pi/2)+atan(abs(dlat)/abs(dlon)) # Assigns angle between this location and other location clockwise from true north
        elif otherlonr<thislonr:
            if otherlatr==thislatr:
                result=(1.5*pi) # Assigns angle between this location and other location clockwise from true north
            elif otherlatr<thislatr:
                result=(pi)+atan(abs(dlon)/abs(dlat)) # Assigns angle between this location and other location clockwise from true north
            elif otherlatr>thislatr:
                result=(1.5*pi)+atan(abs(dlat)/abs(dlon)) # Assigns angle between this location and other location clockwise from true north
        elif otherlonr==thislonr:
            if otherlatr>thislatr:
                result=0 # Assigns angle between this location and other location clockwise from true north
            elif otherlatr<thislatr:
                result=pi # Assigns angle between this location and other location clockwise from true north
        angle=degrees(result) # Converts angle in radians to degrees

        if angle > orientation:
            final_angle = angle - orientation # Angle will be measured clockwise from heading
        else:
            final_angle = orientation - angle # Angle will be measured clockwise from direction of device 2
            final_angle = 360 - final_angle # Angle will be measured clockwise from heading
        angle_to_send = map_function.calc_angle(final_angle)
        OSC_server.send_angle(angle_to_send)
        print(final_angle)
        
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
    
