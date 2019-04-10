'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time
import cv2


from movement import mov
from ColorFinder import findColor
from objFinder import objFind

times = None
movmt = None
finder = None


def setup():

    global times, movmt, finder

    startTime = time.time()

    pickupEnd = startTime + 60 * 2  # 2 minutes

    dumpEnd = pickupEnd + 30  # 30 seconds to dump

    homeEnd = startTime + 60 * 3  # 3 minutes

    times = (startTime, pickupEnd, dumpEnd, homeEnd)

    # Setup the video stream
    capture = cv2.VideoCapture(0)

    # Get the width and height from the capture stream
    w = int(capture.get(3))
    h = int(capture.get(4))

    # Wait for camera to initialize
    time.sleep(2)

    # Grab the first frame
    ret, firstFrame = capture.read()

    # Calculate the home color from the first frame
    homeColor = findColor(firstFrame, 30, 30, (int(w / 2) + 30), h - 20)

    # Explicitly remove first frame to increase free space
    del(firstFrame)

    # Create the object finder
    finder = objFind(capture,homeColor)

    # Initialize Panduino communications
    movmt = mov(w, h)

    # Send home color to Panduino
    movmt.writeArray("h{0}".format(homeColor))

if __name__ == "__main__":
    setup()
    try:

        # Pickup foodstuffs
        while time.time() < times[1]:

            (food, tels) = finder.findObjs(food=True)

            movmt.whereToGo(food, tels)

            movmt.goToWhere()
        # Dump foodstuffs at  location
        while time.time() < dumpEnd[2]:

            (pill, tels) = finder.findObjs(food=False)

            movmt.whereToGo(pill, tels)

            movmt.gotToWhere()
        # Go home quickly
        while time.time() < homeEnd[3]:

            (pill, tels) = finder.findObjs(food=False, goHome=True)

            movmt.whereToGo(pill, tels)

    except (KeyboardInterrupt, ValueError) as e:

        # If there is a keyboard interrupt, tell Panduino to stop
        movmt.writeArray('a0')
        movmt.writeArray('w0')
        movmt.writeArray('z0')

        # Destroy all cv2 windows
        cv2.destroyAllWindows()

        # Close the serial connection
        movmt.ser.close()

        # Exit python
        exit()
