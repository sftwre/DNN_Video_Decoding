import cv2
import imagezmq
import socket
import time
from config import Config


# initialize the ImageSender object with the socket address of the
config = Config()

server_url = f"tcp://{config.gcp_address}:5555"
sender = imagezmq.ImageSender(connect_to=server_url)

# get the host name and initialize the video stream
rpiName = socket.gethostname()

cap = cv2.VideoCapture(config.NYC_VIDEO_PTH)

time.sleep(2.0)

while cap.isOpened():

    # read the frame from the sequence and send it to the server
    rval, frame = cap.read()

    if type(frame).__module__ == 'numpy':
        sender.send_image(rpiName, frame)

cap.release()