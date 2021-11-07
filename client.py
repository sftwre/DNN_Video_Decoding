import os
import cv2
import numpy as np
import socket
import struct
from io import BytesIO
from config import Config

# modified code from https://github.com/rena2damas/remote-opencv-streaming-live-video

config = Config()

# clip to stream
video_pth = os.path.join(config.REDS_PTH, '000')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

# load each frame in clip and send to server
for frame_pth in os.listdir(video_pth):

    frame = cv2.imread(frame_pth)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    memfile = BytesIO()
    np.save(memfile, frame)
    memfile.seek(0)
    data = memfile.read()

    # Send form byte array: frame size + frame content
    client_socket.sendall(struct.pack("L", len(data)) + data)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break