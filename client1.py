import socket
import cv2
import pickle
import struct
import sounddevice as sd
import numpy as np

# Socket Create
family = socket.AF_INET
protocol = socket.SOCK_STREAM
clien = socket.socket(family, protocol)
clien.connect(("192.168.29.148", 8080))

# Function to play audio
def play_audio(audio_data):
    sd.play(audio_data, samplerate=44100, blocking=True)

data = b""
payload_size = struct.calcsize("Q")

# Receiving and displaying video with audio
while True:
    # Receiving video data
    while len(data) < payload_size:
        packet = clien.recv(4096)
        if not packet: 
            break
        data += packet
    
    if len(data) < payload_size:
        print("Incomplete video data received")
        continue
    
    # Unpack payload size for video
    packed_msg = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg)[0]
    
    # Receiving complete video frame
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
    
    # Deserialize video frame
    try:
        frame = pickle.loads(frame_data)
    except pickle.UnpicklingError:
        print("Error: pickle data was truncated")
        continue
    
    # Display video frame
    cv2.imshow("Video from server", frame)
    
    # Receiving audio data
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
    audio_msg_size = struct.unpack("Q", packed_msg)[0]
    
    # Receiving complete audio data
    while len(data) < audio_msg_size:
        packet = clien.recv(4096)
        if not packet: 
            break
        data += packet
    
    if len(data) < audio_msg_size:
        print("Incomplete audio data received")
        continue
    
    # Extract audio data
    audio_data = np.frombuffer(data[:audio_msg_size], dtype=np.float32)
    data = data[audio_msg_size:]
    
    # Play audio
    play_audio(audio_data)
    
    # Listen for termination key
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

clien.close()
