
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time

# TODO: Fix if needed due to no reference video being passed will always
# be webcam (speed on startup concerns)
NUM_SIDES = 10
BLOCK_DIVISION = 100
MIN_VALUE = 30

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
blueLower = (95, 109, 0)
blueUpper = (117, 255, 255)

greenLower = (35, 115, 0)
greenUpper = (86, 255, 255)

yellowLower = (13, 71, 0)
yellowUpper = (26, 255, 255)

redLower = (0, 118, 0)
redUpper = (6, 255, 255)

stLower = (10, 60, 0)
stUpper = (17, 255, 255)

objects = []

colors = {'cntsB': (255, 0, 0), 'cntsY': (0, 255, 255), 'cntsR': (
    0, 0, 255), 'cntsG': (0, 255, 0), 'cntsS': (0, 128, 255)}
# TODO: Removes Arguments from buffer Im pretty sure?
pts = deque(maxlen=args["buffer"])
# TODO: Fix Below code if VideoStream is better at video capture reference to VideoStream class here :https://github.com/jrosebr1/imutils/blob/master/imutils/video/videostream.py
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=1).start()

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
    # grab the current frame
    frame = vs.read()

    # TODO: If above edited fix
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    # TODO: maybe not resize or blur?

    frame = imutils.resize(frame, width=600)
    frame1 = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for blue, green, yellow, and red, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    maskB = cv2.inRange(hsv, blueLower, blueUpper)
    maskB = cv2.erode(maskB, None, iterations=2)
    maskB = cv2.erode(maskB, None, iterations=2)
    maskB = cv2.dilate(maskB, None, iterations=1)
    maskB = cv2.dilate(maskB, None, iterations=2)
    maskB = cv2.dilate(maskB, None, iterations=3)

    maskG = cv2.inRange(hsv, greenLower, greenUpper)
    maskG = cv2.erode(maskG, None, iterations=1)
    maskG = cv2.erode(maskG, None, iterations=2)
    maskG = cv2.dilate(maskG, None, iterations=1)
    maskG = cv2.dilate(maskG, None, iterations=1)
    maskG = cv2.dilate(maskG, None, iterations=1)

    maskY = cv2.inRange(hsv, yellowLower, yellowUpper)
    maskY = cv2.erode(maskY, None, iterations=2)
    maskY = cv2.erode(maskY, None, iterations=2)
    maskY = cv2.dilate(maskY, None, iterations=2)
    maskY = cv2.dilate(maskY, None, iterations=2)
    maskY = cv2.dilate(maskY, None, iterations=2)

    maskR = cv2.inRange(hsv, redLower, redUpper)
    maskR = cv2.erode(maskR, None, iterations=2)
    maskR = cv2.erode(maskR, None, iterations=2)
    maskR = cv2.dilate(maskR, None, iterations=1)
    maskR = cv2.dilate(maskR, None, iterations=2)
    maskR = cv2.dilate(maskR, None, iterations=2)

    maskS = cv2.inRange(hsv, stLower, stUpper)
    maskS = cv2.erode(maskS, None, iterations=2)
    maskS = cv2.erode(maskS, None, iterations=2)
    maskS = cv2.dilate(maskS, None, iterations=2)
    maskS = cv2.dilate(maskS, None, iterations=2)

    # TODO: Remove center initialization code(No point to waste memory here) also again with the videostream
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    dictionary = {}
    dictionary['cntsB'] = cv2.findContours(
        maskB.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dictionary['cntsB'] = dictionary['cntsB'][
        0] if imutils.is_cv2() else dictionary['cntsB'][1]

    dictionary['cntsG'] = cv2.findContours(
        maskG.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dictionary['cntsG'] = dictionary['cntsG'][
        0] if imutils.is_cv2() else dictionary['cntsG'][1]

    dictionary['cntsY'] = cv2.findContours(
        maskY.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dictionary['cntsY'] = dictionary['cntsY'][
        0] if imutils.is_cv2() else dictionary['cntsY'][1]

    dictionary['cntsR'] = cv2.findContours(
        maskR.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dictionary['cntsR'] = dictionary['cntsR'][
        0] if imutils.is_cv2() else dictionary['cntsR'][1]

    blah['cntsS'] = cv2.findContours(
        maskS.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blah['cntsS'] = dictionary['cntsS'][
        0] if imutils.is_cv2() else dictionary['cntsS'][1]

    centerB = None
    food = []
    pill = []
    # only proceed if at least one contour was found
    for key, cnts in dictionary.items():
        if len(dictionary[key]) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            for cB in dictionary[key]:
                approx = cv2.approxPolyDP(
                    cB, 0.01 * cv2.arcLength(cB, True), True)
                if len(approx) <= NUM_SIDES:
                    x, y, w, h = cv2.boundingRect(cB)

                    if not (h > w * 2):
                        food.append((x, y, w, h))
                    else (h > w * 2):
                        pill.append((x, y, w, h))

                elif len(approx) > NUM_SIDES:
                    ((x, y), radius) = cv2.minEnclosingCircle(cB)
                    mB = cv2.moments(cB)
                    # centerB = (int(mB["m10"] / mB["m00"]), int(mB["m01"] / mB["m00"]))
                    # only proceed if the radius meets a minimum size
                    if radiusB * 1.5 > MIN_VALUE:
                        food.append((x, y, 2 * radius, 2 * radius))
    return pill, food
