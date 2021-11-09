import os
import cv2
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
from io import BytesIO
from config import Config


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=False, default='127.0.0.1',
	help="ip address of the server to which the client will connect")

args = ap.parse_args()

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to=f"tcp://{args.server_ip}:5555")

# get the host name and initialize the video stream
rpiName = socket.gethostname()

config = Config()

# video sequence
video_seq_pth = os.path.join(config.REDS_PTH, '000', '%08d.png')
cap = cv2.VideoCapture(video_seq_pth)

# vs = VideoStream(usePiCamera=True).start()
# vs = VideoStream(src=0).start()
time.sleep(2.0)

while cap.isOpened():

    # read the frame from the sequence and send it to the server
    _, frame = cap.read()
    sender.send_image(rpiName, frame)

cap.release()