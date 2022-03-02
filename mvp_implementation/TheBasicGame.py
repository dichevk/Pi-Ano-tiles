import time
#import keyboard
import threading
import sys
from rpi_ws281x import *
import argparse
import serial

# LED strip configuration:
LED_COUNT      = 40      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 25     # Set to 0 for darkest and 255 for brightest
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
        Play()

#kbrdInput = inputThread(1, "Input_Thread", 1)

tileFeeder = []
beat_frequency = 0

def loadFile(song):
    txt = ".txt"
    filename = song + txt
    with open(filename, 'r') as filehandle:
        filecontents = filehandle.readlines()
        for i in range(len(filecontents)):
            # remove linebreak which is the last character of the string
            if i == 0:
                beat_frequency = filecontents[0][:-1]
            else:
                current_row = filecontents[i][:-1]
                temp = []
                # add item to the list
                for i in range(len(current_row)):
                    temp.append(current_row[i])
                tileFeeder.append(temp)

ledStrip = ["-", "-", "-", "-", "-", "-", "-", "-", "-",
            "-","-", "-", "-", "-", "-", "-", "-", "-", "-",
            "-","-", "-", "-", "-", "-", "-", "-", "-", "-",
            "-","-", "-", "-", "-", "-", "-", "-", "-", "-",
            "-"]

firstRow = [0, 19, 20, 39]
lastRow = [9,10,29,30]

score = 0
songName = ""

pressedSomething = True
smthingToPress = True
gameRunning = False
wrongButton = False

def inputHandler():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.001)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            #time.sleep(0.1)          
            line = ser.readline().decode('utf-8').rstrip()
            if gameRunning:
                if line < 4:
                    pressedSomething = True
                    if ledStrip[lastRow[line-1]] == "+":
                        score+=1
                        continue
                    else:
                        wrongButton = True
                else:
                    continue
            else:
                if line < 4:
                    continue
                else:
                    songName = "CreativeMinds"
                    if songName != "":
                        gameRunning = True
                        kbrdInput.daemon = True
                        kbrdInput.start()
                        Play()
                    else:
                        continue

                    






def clearStrip(strip, PIN_NUM):
    strip.setPixelColor(PIN_NUM, Color(0,0,0))
    strip.show()

def lightUp(strip,PIN_NUM):
    strip.setPixelColor(PIN_NUM,Color(0,128,0))
    strip.show()

def printCanvas():
    for i in range(10):
        print(ledStrip[i], "", ledStrip[19-i], "",
              ledStrip[i+20], "", ledStrip[39-i])

def updateLedStrip():
    for i in range(len(ledStrip)):
        if(ledStrip[i] == "+"):
            lightUp(strip, i)
        else:
            clearStrip(strip, i)


def Play():
    loadFile(songName)
    global pressedSomething
    global smthingToPress
    global gameRunning
    gameRunning = True
    #SetDisplay(songName)
    for incomingRow in range(len(tileFeeder)):
        if wrongButton == False:
            for column in lastRow:
                if ledStrip[column] == "+":
                    smthingToPress = True
                    break
            if pressedSomething == False and smthingToPress:
                print("You missed a tile")
                gameRunning = False
                break
            smthingToPress = False
            pressedSomething = False
            for i in range(9):
                ledStrip[9-i] = ledStrip[8-i]
                ledStrip[10+i] = ledStrip[11+i]
                ledStrip[29-i] = ledStrip[28-i]
                ledStrip[30+i] = ledStrip[31+i]
            for i in range(len(tileFeeder[incomingRow])):
                ledStrip[firstRow[i]] = tileFeeder[incomingRow][i]
            #printCanvas()
            updateLedStrip()
            if incomingRow != len(tileFeeder)-1:
                time.sleep(beat_frequency)
            else:
                print("You completed the level")
                gameRunning = False
                break
        else:
            gameRunning = False
            print("You pressed wrong button and/or in the wrong time")
            break

inputHandler()

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
