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

tileFeeder = []
beat_frequency = 0
#----- Altered LCD code ---------------------------
# requires RPi_I2C_driver.py
#import RPi_I2C_driver
#from time import *


songNames = ["CreativeMinds", "House", "Moose", "SlowMotion"]

#lcd = RPi_I2C_driver.lcd()

# updates currentscore or display final score. If finalscore == -1, currentscore is displayed. If currenscore == -1, the game is over and finalscore is displayed
def LCDDisplay(currentScore, finalScore):
    
    if currentScore >= 0 and finalScore == -1:  # only changes line 3, song name and "current score:" stay on display
        currentScore_as_string = str(currentScore)
        print('        ' + currentScore_as_string, 3)
    elif currentScore == -1 and finalScore >= 0:    # erase display and show final score
        print("------- LCD --------")
        finalScore_as_string = str(finalScore)
        print('  Final Score:', 2)
        print('        ' + finalScore_as_string, 3)
    else:
        print("fault in score (currentscore/finalscore)")

# Before starting game, call setDisplay to display the song name on line 1, and "current score:" on line 2.     
def SetDisplay(songName):
    print("------- LCD --------")
    print(songName, 1)
    print('  Current Score:', 2)

def displayMenu1(i):
    print('>'+songNames[i])
    print(songNames[i+1])
    print(songNames[i+2])
    print(songNames[i+3])

def displayMenu2(i):
    print(songNames[i-1])
    print('>'+songNames[i])
    print(songNames[i+1])
    print(songNames[i+2])

def displayMenu3(i):
    print(songNames[i-2])
    print(songNames[i-1])
    print('>'+songNames[i])
    print(songNames[i+1])

def displayMenu4(i):
    print(songNames[i-3])
    print(songNames[i-2])
    print(songNames[i-1])
    print('>'+songNames[i])

# possible actions: -1 = init, 4 = back/up, 5 = select, 6 = right/down
# if action == 5 (select), then returns index of song in the array SongNames that is currently selected
pos = 0
max = len(songNames)-1

def SelectSong(action):
    global songName
    #-- print(clear)()
    print("------- LCD --------")
    global pos
    if action == -1: # = init
        displayMenu1(0)
    if action == 4: # back/up      
        if pos == 0:
            displayMenu1(0)
        elif pos == max:
            pos = pos -1
            displayMenu3(pos)
        elif pos == max-1:
            pos = pos -1
            displayMenu2(pos)
        elif 0<pos<=max-2:
            pos = pos -1
            displayMenu1(pos)
    if action == 6: # forward/down
        if 0<= pos <max-3:
            pos = pos +1
            displayMenu1(pos)
        elif pos == max:
            displayMenu4(pos)
        elif pos == max-1:
            pos = pos +1
            displayMenu4(pos)
        elif pos==max-2:
            pos = pos +1
            displayMenu3(pos)
        elif pos == max-3:
            pos = pos +1
            displayMenu2(pos)
    if action == 5: # select
        songName = songNames[pos]            

def loadFile(song):
    global beat_frequency
    txt = ".txt"
    print("song:" + song)
    filename = song + txt
    with open(filename, 'r') as filehandle:
        filecontents = filehandle.readlines()
        for i in range(len(filecontents)):
            # remove linebreak which is the last character of the string
            if i == 0:
                beat_frequency = float(filecontents[0][:-1])
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

tileFeeder = []
score = 0
songName = ""
pressedSomething = True
smthingToPress = True
gameRunning = False
wrongButton = False
tileFeeder = []
beat_frequency = 0

def resetVars():
    global tileFeeder
    global score
    global songName
    global pressedSomething
    global smthingToPress
    global gameRunning
    global wrongButton
    global tileFeeder
    global beat_frequency
    SelectSong(-1)
    tileFeeder = []
    score = 0
    pressedSomething = True
    smthingToPress = True
    gameRunning = False
    wrongButton = False
    tileFeeder = []
    beat_frequency = 0

def inputHandler():
    global gameRunning
    global songName
    global score
    global wrongButton
    global pressedSomething
    global ledStrip
    global lastRow
    global beat_frequency
    inputHandler
    SelectSong(-1)
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.005)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            #time.sleep(0.1)          
            line = ser.readline().decode('utf-8').rstrip()
            #print(line)
            if gameRunning:
                if int(line) < 4:
                    pressedSomething = True
                    if ledStrip[lastRow[int(line)]] == "+":
                        score+=1
                        LCDDisplay(score,-1)
                        beat_frequency = beat_frequency*0.97
                        #print("beatfreq = "+str(beat_frequency))
                        continue
                    else:
                        LCDDisplay(-1,score)
                        wrongButton = True 
                        #Wrong button colored
                        if int(line) == 0:
                            wrongLed(strip,9)
                        if int(line) == 1:
                            wrongLed(strip,10)
                        if int(line) == 2:
                            wrongLed(strip,29)
                        if int(line) == 3:
                            wrongLed(strip,30)
                else:
                    continue
            else:
                if int(line) < 4:
                    continue
                else:
                    SelectSong(int(line))
                    #Song is selected
                    if songName != "":
                        resetVars()
                        gameRunning = True
                        gameHandler = inputThread(1, "Input_Thread", 1)
                        #gameHandler.daemon = True
                        gameHandler.start()
                    else:
                        continue
        elif gameRunning == False:
            idleLeds(strip)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

inActive = 0
def idleLeds(strip):
    global inActive
    if inActive > 4:
        strip.setPixelColor(inActive-5, Color(0,0,0))
    else:
        strip.setPixelColor(LED_COUNT-4+inActive, Color(0,0,0))
    strip.setPixelColor(inActive, wheel(inActive*6))
    strip.show()
    inActive += 1
    if inActive > LED_COUNT:
        inActive = 0
    time.sleep(0.1)

def clearStrip(strip, PIN_NUM):
    strip.setPixelColor(PIN_NUM, Color(0,0,0))
    strip.show()

def wrongLed(strip, PIN_NUM):
    for x in range(3):
        strip.setPixelColor(PIN_NUM, Color(128,0,0))
        strip.show()
        time.sleep(0.3)
        strip.setPixelColor(PIN_NUM, Color(0,0,0))
        strip.show()
        time.sleep(0.3)

def lightUp(strip,PIN_NUM):
    if PIN_NUM == 9 or PIN_NUM == 10 or PIN_NUM == 29 or PIN_NUM == 30:
        strip.setPixelColor(PIN_NUM,Color(0,0,128))
    else:
        #strip.setPixelColor(PIN_NUM,Color(0,128,0))
        #strip.setPixelColor(PIN_NUM,wheel(PIN_NUM*5))   #Rainbow colors

        if PIN_NUM >= 0 and PIN_NUM < 10:       #row 1
            strip.setPixelColor(PIN_NUM,wheel(80+PIN_NUM*8))
        elif PIN_NUM >= 10 and PIN_NUM < 20:    #row 2
            strip.setPixelColor(PIN_NUM,wheel(80+(19-PIN_NUM)*8))
        elif PIN_NUM >= 20 and PIN_NUM < 30:    #row 3
            strip.setPixelColor(PIN_NUM,wheel(80+(PIN_NUM-20)*8))
        elif PIN_NUM >= 30 and PIN_NUM < 40:    #row 4
            strip.setPixelColor(PIN_NUM,wheel(80+(39-PIN_NUM)*8))
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
    global songName
    loadFile(songName)
    global pressedSomething
    global smthingToPress
    global gameRunning
    global beat_frequency
    gameRunning = True
    nextLed = 0
    #SetDisplay(songName)
    for incomingRow in range(len(tileFeeder)):
        if wrongButton == False:
            for column in lastRow:
                if ledStrip[column] == "+":
                    smthingToPress = True
                    nextLed = column
                    break
            if pressedSomething == False and smthingToPress:
                print("You missed a tile")
                #Wrong button colored
                wrongLed(strip,nextLed)
                gameRunning = False
                songName = ""
                SelectSong(-1)
                for i in range(len(ledStrip)):
                    ledStrip[i] = "-"
                updateLedStrip()
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
                songName = ""
                SelectSong(-1)
                break
        else:
            time.sleep(0.9)
            gameRunning = False
            songName = ""
            SelectSong(-1)
            print("You pressed wrong button and/or in the wrong time")
            
            for i in range(len(ledStrip)):
                ledStrip[i] = "-"
            updateLedStrip()
            break

inputHandler()