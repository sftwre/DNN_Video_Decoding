

class Config:
    """
    Configuration file for project with paths to video assets and GCP compute IP addresses
    """

    def __init__(self):
        self.REDS_PTH = '../REDS_dataset/train_sharp_bicubic/X4'
        self.NYC_VIDEO_PTH = '../video/NYCIntersection-20sec.mp4'