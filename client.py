import socket
import cv2
import pickle
import struct

#providing server ip and port
family = socket.AF_INET
protocol = socket.SOCK_STREAM
clien = socket.socket(family, protocol)
clien.connect(("172.16.2.10", 7878))

data = b""
payload_size = struct.calcsize("Q")

# sending our photo in a loop to the server
while True:
    while len(data) < payload_size:
        packet = clien.recv(4096)
        
        if not packet: 
            break
        data+=packet
    packed_msg = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg)[0]
    
    while len(data) < msg_size:
        data += clien.recv(4096)
    frame = data[:msg_size]
    data  = data[msg_size:]
    vid = pickle.loads(frame)
    cv2.imshow("Video from server",vid)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
clien.close()