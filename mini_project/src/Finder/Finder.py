import numpy.core.multiarray
from picamera import PiCamera
from time import sleep
from cv2 import aruco
import cv2
import io
import numpy as np

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

class Finder:
    def __init__(self):
        # Init function sets up camera
        self.camera = PiCamera()
        # Make resolution smaller to increase speed, larger to increase accuracy
        self.camera.resolution = (800, 600)
        #self.camera.resolution = (1920, 1080)
        self.camera.exposure_mode = 'off'
        self.camera.shutter_speed = 10000
        self.camera.awb_mode = 'off'

    def find_markers(self):
        # Image is captured to bit stream and decoded
        img_stream = io.BytesIO()
        self.camera.capture(img_stream, 'jpeg')
        img_stream.seek(0)
        img_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        # Image is converted to grayscale first
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Thresholding is used to convert to a binary image
        # Otsu's method maximizes contrast based on the input image
        # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        thresh = cv2.equalizeHist(gray)

        # Use built-in detection method
        x = aruco.detectMarkers(thresh, aruco_dict)

        # Determine locations of quadrants in image
        mid_y, mid_x = gray.shape
        mid_x /= 2
        mid_y /= 2

        quadrants = []

        # Run if markers are detected
        if x[1] is not None:
            for i in range(len(x[1])):
                marker_id = x[1][i][0]
                corners = x[0][i][0]

                # Find center of marker in image
                x0, y0 = corners[0]
                x1, y1 = corners[1]
                x2, y2 = corners[2]
                x3, y3 = corners[3]
                avg_x = (x0 + x1 + x2 + x3) / 4
                avg_y = (y0 + y1 + y2 + y3) / 4

                # Check for each quadrant
                if avg_y < mid_y:
                    if avg_x > mid_x:
                        quadrants.append((marker_id, 1))
                    else:
                        quadrants.append((marker_id, 2))
                else:
                    if avg_x > mid_x:
                        quadrants.append((marker_id, 4))
                    else:
                        quadrants.append((marker_id, 3))

        return quadrants
            
