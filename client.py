import os
import cv2
import numpy as np
import socket
import struct
from io import BytesIO
from config import Config

# modified code from https://github.com/rena2damas/remote-opencv-streaming-live-video

config = Config()

# video sequence
video_seq_pth = os.path.join(config.REDS_PTH, '000', '%08d.png')
cap = cv2.VideoCapture(video_seq_pth)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

# load each frame in clip and send to server
while cap.isOpened():

    _, frame = cap.read()

    memfile = BytesIO()
    np.save(memfile, frame)
    memfile.seek(0)
    data = memfile.read()

    # Send form byte array: frame size + frame content
    client_socket.sendall(struct.pack("L", len(data)) + data)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()