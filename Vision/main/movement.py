'''

This is where the code for communicating to the movement arduino will go.

WSAD + Z followed by an int 0 to 255

h + {rgby} to set home color

W255 = FASTEST FORWARD PLZ
A255 = FASTEST LEFT PLZ (Turn on a dime)
S
D
Z0 = STOP

'''

import time
import serial
import math


class mov:

    def __init__(self, w, h):
        self.ser = serial.Serial(
            port='/dev/ttyACM0', baudrate=115200, writeTimeout=0)

        self.w = w
        self.halfW = w / 2
        self.h = h
        self.gravConst = 1

    def writeArray(self, value):

        print(value)

        # Uncomment below when actually running
        self.ser.isOpen()
        self.ser.write(value.encode())

    def goToWhere(self):
        for i in self.values:
            self.writeArray(i)
            time.sleep(.001)

    def findTurn(self, objLoc, objgrav):

        totalTurn = 0
        # for obj in objLoc:
        x, y = objLoc
        if x == -1:
            return 0, False

        turn = ((x - self.halfW) / self.halfW) * \
            ((self.h - y) / self.h) * self.gravConst * objgrav
        #totalTurn += turn

        # return totalTurn/len(objLoc), True

        return turn, True

    def search(SpaceTels=False):
        '''
        Hey Matt, this is the code you need to write. It should move backwards and look left and right depending on how often it's been called. You can keep track using a new variable self.foo.

        This bypasses all space tel finder code, so be careful. If you want to try and incorporate tel finder go for it.

        I've passed the SpaceTels boolean so you can try to do something with that.

        Good luck,
        if you need help lemme know
        G
        '''

        print("MATT")

        # yDirec = a or d
        # xDirec = w or s

        self.values = [yDirec, xDirec]
        return (yDirec, xDirec)

    def whereToGo(self, food, tels):
        speedScale = 127

        # print(food)

        foodDirection, foodEx = self.findTurn(food, 1.0)
        telDirection, telEx = self.findTurn(tels, -.75)

        if telEx and foodEx:
            numObj = 2
        elif foodEx:
            numObj = 1
        elif telEx:
            return self.search(True)
            numObj = 1
        else:
            return self.search(False)  # TODO this cant do nothing ##Cant it?

        direction = foodDirection + telDirection  # to keep under 1.0 may need mods

        if direction < 0:
            mappedVal = int((-speedScale * direction) / numObj)

            xDirec = "a{0}".format(mappedVal)
        else:
            mappedVal = int((speedScale * direction) / numObj)

            xDirec = "d{0}".format(mappedVal)

        yDirec = "w{0}".format(int(speedScale * (1 - abs(direction))))

        self.values = [yDirec, xDirec]
        return(yDirec, xDirec)

if __name__ == "__main__":
    m = mov(600, 600)
    #print(m.whereToGo([(100, 100), (300, 300)], [(100,100)])[0])
    #print(m.whereToGo([(200, 200)], []))
    print(m.whereToGo((200, 200), (-1, -1)))
