import os
import cv2
from imutils.video import VideoStream
import imagezmq
import socket
import time
from io import BytesIO
from config import Config


# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to=f"tcp://127.0.0.1:5555")

# get the host name and initialize the video stream
rpiName = socket.gethostname()

config = Config()
cap = cv2.VideoCapture(config.NYC_VIDEO_PTH)

time.sleep(2.0)

while cap.isOpened():

    # read the frame from the sequence and send it to the server
    rval, frame = cap.read()

    if type(frame).__module__ == 'numpy':
        sender.send_image(rpiName, frame)

cap.release()