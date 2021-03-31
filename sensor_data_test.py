import socket, traceback

host = '192.168.21.110'
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

while 1:
    try:
        message, address = s.recvfrom(8192)
        y = message.decode("utf-8") # Standard encoding for characters. y holds useful data
        if ' 81, ' in y:
            keyword = ' 81, '
            before_keyword, keyword, after_keyword = y.partition(keyword)
            orientation = after_keyword[0:7]
            if after_keyword[0] == ' ':
                orientation = after_keyword[1:7]
            if after_keyword[1] == ' ':
                orientation = after_keyword[2:7]
            print(orientation)
        


    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
