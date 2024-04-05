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
        while(cap.isOpened()):
            # Capture video frame
            ret, frame = cap.read()
            if not ret:
                break
            
            # Capture audio
            audio_data = record_audio()
            
            # Serialize video frame
            video_data = pickle.dumps(frame)
            video_message = struct.pack("Q", len(video_data)) + video_data
            
            # Serialize audio data
            audio_data_bytes = audio_data.tobytes()
            audio_message = struct.pack("Q", len(audio_data_bytes)) + audio_data_bytes
            
            # Send video and audio messages
            try:
                clien.sendall(video_message + audio_message)
            except ConnectionResetError:
                print("Connection reset by peer")
                break
            
            # Listen for termination key
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                clien.close()
                break

        cap.release()
