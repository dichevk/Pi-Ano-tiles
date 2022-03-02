# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *


songNames = ["Impearial_March", "Nutcracker.mp3", "Moonlight_Sonata.mp3", "never gonna give you", "song 5", "give it up", "vrijheid 2"]

lcd = RPi_I2C_driver.lcd()

# updates currentscore or display final score. If finalscore == -1, currentscore is displayed. If currenscore == -1, the game is over and finalscore is displayed
def LCDDisplay(currentScore, finalScore):
    
    if currentScore >= 0 and finalScore == -1:  # only changes line 3, song name and "current score:" stay on display
        currentScore_as_string = str(currentScore)
        lcd.lcd_display_string('        ' + currentScore_as_string, 3)
    elif currentScore == -1 and finalScore >= 0:    # erase display and show final score
        lcd.lcd_clear()
        finalScore_as_string = str(finalScore)
        lcd.lcd_display_string('  Final Score:', 2)
        lcd.lcd_display_string('        ' + finalScore_as_string, 3)
    else:
        print("fault in score (currentscore/finalscore)")

# Before starting game, call setDisplay to display the song name on line 1, and "current score:" on line 2.     
def SetDisplay(songName):
    lcd.lcd_clear()
    lcd.lcd_display_string(songName, 1)
    lcd.lcd_display_string('  Current Score:', 2)

# To test setDisplay:
"""
song = "test song name"
SetDisplay(song)
sleep(1)
LCDDisplay(2, -1)
sleep(1)
LCDDisplay(4, -1)
sleep(1)
LCDDisplay(8, -1)
sleep(1)
LCDDisplay(10, -1)
sleep(1)
LCDDisplay(25, -1)
sleep(2)
LCDDisplay(-1, 26)
"""

def displayMenu1(i):
    lcd.lcd_clear
    lcd.lcd_display_string('>'+songNames[i], 1)
    lcd.lcd_display_string(songNames[i+1], 2)
    lcd.lcd_display_string(songNames[i+2], 3)
    lcd.lcd_display_string(songNames[i+3], 4)

def displayMenu2(i):
    lcd.lcd_clear
    lcd.lcd_display_string(songNames[i-1], 1)
    lcd.lcd_display_string('>'+songNames[i], 2)
    lcd.lcd_display_string(songNames[i+1], 3)
    lcd.lcd_display_string(songNames[i+2], 4)

def displayMenu3(i):
    lcd.lcd_clear
    lcd.lcd_display_string(songNames[i-2], 1)
    lcd.lcd_display_string(songNames[i-1], 2)
    lcd.lcd_display_string('>'+songNames[i], 3)
    lcd.lcd_display_string(songNames[i+1], 4)

def displayMenu4(i):
    lcd.lcd_clear
    lcd.lcd_display_string(songNames[i-3], 1)
    lcd.lcd_display_string(songNames[i-2], 2)
    lcd.lcd_display_string(songNames[i-1], 3)
    lcd.lcd_display_string('>'+songNames[i], 4)

# possible actions: -1 = init, 4 = back/up, 5 = select, 6 = right/down
# if action == 5 (select), then returns index of song in the array SongNames that is currently selected
pos = 0
max = len(songNames)-1
def SelectSong(action):
    lcd.lcd_clear()
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
        return pos            

# TEST selectsong
SelectSong(-1) #put init menu on display    
while 1 == 1:
        print "selected:"+ str(SelectSong(input()))
        

