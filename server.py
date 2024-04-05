import socket
import cv2
import pickle
import struct

# Socket Create
family = socket.AF_INET
protocol = socket.SOCK_STREAM
serv = socket.socket(family, protocol)

# binding ip address with the port
serv.bind(('0.0.0.0', 8080))
serv.listen(5)

#sending photo as a video to the client
while True:
    clien, addr = serv.accept()
    if clien:
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            img,frame = cap.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            clien.sendall(message)
            # cv2.imshow('Video from Server',frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                clien.close()