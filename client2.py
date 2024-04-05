import socket
import cv2
import numpy as np
import struct
import sounddevice as sd

# Socket Create
family = socket.AF_INET
protocol = socket.SOCK_STREAM
clien = socket.socket(family, protocol)
clien.connect(("192.168.93.80", 8080))

# Function to play audio
def play_audio(audio_data):
    sd.play(audio_data, samplerate=44100, blocking=False)

# Receiving and displaying video with audio
while True:
    # Receive video data
    data = b""
    payload_size = struct.calcsize("L")
    while len(data) < payload_size:
        packet = clien.recv(4096)
        if not packet: 
            break
        data += packet
    
    if len(data) < payload_size:
        print("Incomplete data received")
        continue
    
    # Unpack payload size for video
    packed_msg = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg)[0]
    
    # Receive complete video frame
    while len(data) < msg_size:
        packet = clien.recv(4096)
        if not packet: 
            break
        data += packet
    
    if len(data) < msg_size:
        print("Incomplete video data received")
        continue
    
    # Extract video data
    frame_data = data[:msg_size]
    data = data[msg_size:]
    
    # Decode video frame
    frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    # Display video frame
    cv2.imshow("Video from server", frame)
    
    # Receive audio data
    payload_size = struct.calcsize("L")
    while len(data) < payload_size:
        packet = clien.recv(4096)
        if not packet: 
            break
        data += packet
    
    if len(data) < payload_size:
        print("Incomplete audio data received")
        continue
    
    # Unpack payload size for audio
    packed_msg = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg)[0]
    
    # Receive complete audio data
    while len(data) < msg_size:
        packet = clien.recv(4096)
        if not packet: 
            break
        data += packet
    
    if len(data) < msg_size:
        print("Incomplete audio data received")
        continue
    
    # Extract audio data
    audio_data = np.frombuffer(data[:msg_size], dtype=np.float32)
    data = data[msg_size:]
    
    # Play audio
    play_audio(audio_data)
    
    # Listen for termination key
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

clien.close()
