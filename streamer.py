import cv2
import numpy
import socket
import struct
import threading
from io import BytesIO


class Streamer(threading.Thread):

    def __init__(self, hostname, port):
        threading.Thread.__init__(self)

        self.hostname = hostname
        self.port = port
        self.running = False
        self.streaming = False
        self.png = None

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        s.bind((self.hostname, self.port))
        print('Socket bind complete')

        payload_size = struct.calcsize("L")

        s.listen(10)
        print('Socket now listening')

        self.running = True

        while self.running:

            print('Start listening for connections...')

            conn, addr = s.accept()
            print("New connection accepted.")

            while True:

                data = conn.recv(payload_size)

                if data:
                    # Read frame size
                    msg_size = struct.unpack("L", data)[0]

                    # Read the payload (the actual frame)
                    data = b''
                    while len(data) < msg_size:
                        missing_data = conn.recv(msg_size - len(data))
                        if missing_data:
                            data += missing_data
                        else:
                            # Connection interrupted
                            self.streaming = False
                            break

                    # Skip building frame since streaming ended
                    if self.png is not None and not self.streaming:
                        continue

                    # Convert the byte array to a 'png' format
                    memfile = BytesIO()
                    memfile.write(data)
                    memfile.seek(0)
                    frame = numpy.load(memfile, allow_pickle=True)

                    ret, png = cv2.imencode('.png', frame)

                    # transpose color channels
                    # self.png = cv2.cvtColor(png, cv2.COLOR_BGR2RGB)
                    self.png = png
                    self.streaming = True
                else:
                    conn.close()
                    print('Closing connection...')
                    self.streaming = False
                    self.running = False
                    self.png = None
                    break

        print('Exit thread.')

    def stop(self):
        self.running = False

    def get_png(self):
        return self.png.tobytes()
