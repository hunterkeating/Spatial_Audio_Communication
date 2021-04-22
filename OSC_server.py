from pythonosc.udp_client import SimpleUDPClient

def send_angle(message):
    ip = "127.0.0.1" # 127.0.0.1 is localhost
    port = 6789

    client = SimpleUDPClient(ip, port) # Creating the OSC UDP Client

    #print("Sending to Max")
    client.send_message(":", message)
    #print("Angle Sent")

# send_angle('157') # For debugging
