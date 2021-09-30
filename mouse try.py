# import the necessary packages
import cv2
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
# import Tkinter
import imutils
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",	help="OpenCV object tracker type")
args = vars(ap.parse_args())

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(cv2.__version__)
# initialize a dictionary that maps strings to their corresponding
# Recieving the Tracker type
global tracker_type
tracker_type = input("please input a tracker type (BOOSTING, MIL, KCF, TLD, MEDIANFLOW, CSRT, MOSSE): ").upper()



# grab the appropriate object tracker using our dictionary of
# OpenCV object tracker objects
# tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
# initialize the bounding box coordinates of the object we are going
# to track
initBB = None


def nothing(x):
    pass

def mouse_drawing(event, x, y, flags, params):
    global point1, point2, drawing, res_width, res_height, initBB, tracker
    # tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']

    if event == cv2.EVENT_LBUTTONDOWN:
        point1 = (x-B_Box_width, y-B_Box_height)
        point2 = (x+B_Box_width, y+B_Box_height)
        initBB = (x-B_Box_width, y-B_Box_height, x+B_Box_width-(x-B_Box_width) , y+B_Box_height - (y-B_Box_height))
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'CSRT':
            tracker = cv2.TrackerCSRT_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        tracker.init(frame, initBB)

cap = cv2.VideoCapture("traffic.mp4")
cv2.namedWindow("Trackbars")
# cv2.createTrackbar("X-Size", "Trackbars", 1, 3, nothing)
# cv2.createTrackbar("Y-Size", "Trackbars", 1, 3, nothing)
cv2.createTrackbar("Size", "Trackbars", 0, 3, nothing)
# Can add buttons however QT have to be installed
# cv2.createButton("KCF", nothing, None, cv2.QT_PUSH_BUTTON, 1)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

# x_size = cv2.getTrackbarPos("X-Size", "Trackbars")
# y_size = cv2.getTrackbarPos("Y-Size", "Trackbars")
modulation = cv2.getTrackbarPos("Size", "Trackbars")
if modulation == 1:
    B_Box_width = round(cap.get(3) / 40)
    B_Box_height = round(cap.get(4) / 40)
elif modulation == 2:
    B_Box_width = round(cap.get(3) / 60)
    B_Box_height = round(cap.get(4) / 60)
elif modulation == 3:
    B_Box_width = round(cap.get(3) / 80)
    B_Box_height = round(cap.get(4) / 80)
# top = Tkinter.Tk()
while True:
    key = cv2.waitKey(1)
    _, frame = cap.read()
    # Get trackbars Value
    # x_size = cv2.getTrackbarPos("X-Size", "Trackbars")
    # y_size = cv2.getTrackbarPos("Y-Size", "Trackbars")
    modulation = cv2.getTrackbarPos("Size", "Trackbars")
    if modulation == 1:
        B_Box_width = round(cap.get(3) / 40)
        B_Box_height = round(cap.get(4) / 40)
    elif modulation == 2:
        B_Box_width = round(cap.get(3) / 60)
        B_Box_height = round(cap.get(4) / 60)
    elif modulation == 3:
        B_Box_width = round(cap.get(3) / 80)
        B_Box_height = round(cap.get(4) / 80)
    # round numbers for box size
    # B_Box_width = round(cap.get(3) / modulation) # x_size
    # B_Box_height = round(cap.get(3) / modulation) # y_size

    if initBB:  # check if there is tracking began
        fps = FPS().start()
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # update the FPS counter
        fps.update()
        fps.stop()
        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, 100 - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(10)
    if key == 27:
        break
    elif key == 32:
        tracker_type = input("please input a tracker type (BOOSTING, MIL, KCF, TLD, MEDIANFLOW, CSRT, MOSSE): ").upper()

cap.release()
cv2.destroyAllWindows()