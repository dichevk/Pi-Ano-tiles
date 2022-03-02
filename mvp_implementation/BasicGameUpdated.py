import time
#import keyboard
import threading
import sys
from rpi_ws281x import *
import argparse
import serial

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

class inputThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        inputHandler()

#kbrdInput = inputThread(1, "Input_Thread", 1)

tileFeeder = [["+", "-", "-", "-"], ["-", "+", "-", "-"], ["-", "-", "-", "+"], ["-", "-", "+", "-"], ["-", "+", "-", "-"],
              ["-", "-", "+", "+"],["-", "-", "-", "+"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"], ["-", "-", "-", "-"]]
ledStrip = ["-", "-", "-", "-", "-", "-", "-", "-", "-",
            "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","-", "-", "-", "-", "-", "-", "-", "-", "-",
            "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","-", "-", "-", "-", "-", "-", "-", "-", "-",
            "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]

firstRow = [0, 29, 30, 59]
lastRow = [14,15,44,45]

pressedSomething = True
smthingToPress = True

def inputHandler():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.001)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            pressedSomething = True
            #time.sleep(0.1)          
            line = ser.readline().decode('utf-8').rstrip()
            if ledStrip[lastRow[line-1]] == "+":
                continue
            else:
                break


def clearStrip(strip, PIN_NUM):
    strip.setPixelColor(PIN_NUM, Color(0,0,0))
    strip.show()

def lightUp(strip,PIN_NUM):
    strip.setPixelColor(PIN_NUM,Color(0,128,0))
    strip.show()

def printCanvas():
    for i in range(15):
        print(ledStrip[i], "", ledStrip[29-i], "",
              ledStrip[i+30], "", ledStrip[59-i])

def updateLedStrip():
    for i in range(len(ledStrip)):
        if(ledStrip[i] == "+"):
            lightUp(strip, i+1)
        else:
            clearStrip(strip, i+1)


def Play():
    global pressedSomething
    global smthingToPress
    #kbrdInput.daemon = True
    #kbrdInput.start()
    for incomingRow in range(len(tileFeeder)):
        '''if kbrdInput.is_alive():
            for column in lastRow:
                if ledStrip[column] == "+":
                    smthingToPress = True
                    break
            if pressedSomething == False and smthingToPress:
                print("You missed a tile")
                break'''
        smthingToPress = False
        pressedSomething = False
        for i in range(14):
            ledStrip[14-i] = ledStrip[13-i]
            ledStrip[15+i] = ledStrip[16+i]
            ledStrip[44-i] = ledStrip[43-i]
            ledStrip[45+i] = ledStrip[46+i]
        for i in range(len(tileFeeder[incomingRow])):
            ledStrip[firstRow[i]] = tileFeeder[incomingRow][i]
        #printCanvas()
        updateLedStrip()
        if incomingRow != len(tileFeeder)-1:
            time.sleep(1)
        else:
            print("You completed the level")
            break
        '''else:
            print("You pressed wrong button and/or in the wrong time")
            break'''
    sys.exit()

Play()

'''def processInput():
    global pressedSomething
    while True:
        if keyboard.is_pressed('a'):
            
            if ledStrip[14] == "+":pressedSomething = True
                continue
            else:
                break
        elif keyboard.is_pressed('s'):
            pressedSomething = True
            if ledStrip[15] == "+":
                continue
            else:
                break
        elif keyboard.is_pressed('d'):
            pressedSomething = True
            if ledStrip[44] == "+":
                continue
            else:
                break
        elif keyboard.is_pressed('f'):
            pressedSomething = True
            if ledStrip[45] == "+":
                continue
            else:
                break
        else:
            continue'''
