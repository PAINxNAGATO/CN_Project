import socket
import cv2
import pickle
import struct
import sounddevice as sd
import numpy as np

# Socket Create
family = socket.AF_INET
protocol = socket.SOCK_STREAM
serv = socket.socket(family, protocol)

# binding ip address with the port
serv.bind(('0.0.0.0', 8080))
serv.listen(5)

# Function to record audio
def record_audio():
    samplerate = 44100  # Sample rate
    duration = 1  # seconds
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype='float32')
    sd.wait()
    return recording

#sending photo and audio as video to the client
while True:
    clien, addr = serv.accept()
    if clien:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set video width
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # Set video height
        cap.set(cv2.CAP_PROP_FPS, 30)           # Set frames per second
        
        while(cap.isOpened()):
            # Capture video frame
            ret, frame = cap.read()
            if not ret:
                break
            
            # Capture audio
            audio_data = record_audio()
            
            # Serialize video frame
            ret, encoded_frame = cv2.imencode('.jpg', frame)
            video_data = encoded_frame.tobytes()
            video_message = struct.pack("L", len(video_data)) + video_data
            
            # Serialize audio data
            audio_data_bytes = audio_data.tobytes()
            audio_message = struct.pack("L", len(audio_data_bytes)) + audio_data_bytes
            
            # Send video and audio messages
            try:
                clien.sendall(video_message + audio_message)
            except ConnectionResetError:
                print("Connection reset by peer")
                break

        cap.release()
