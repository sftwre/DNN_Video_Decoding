import cv2
import imagezmq

class Streamer:
    """"
    Streams video frames from a remote client in a separate thread
    using an ZMQ ImageHub broker.
    """

    def __init__(self):

        # connection to message broker
        self.imageHub = imagezmq.ImageHub()

    def get_jpeg(self):

        (rpiName, frame) = self.imageHub.recv_image()

        # send ACK
        self.imageHub.send_reply(b'OK')

        if type(frame).__module__ == 'numpy':

            print(f'Received video frame, shape - {frame.shape}')

            return cv2.imencode('.jpg', frame)[1].tobytes()
        else:
            print('Video stream ended, closing connection...')
            self.imageHub.close()

        return None

