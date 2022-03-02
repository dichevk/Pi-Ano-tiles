# Imports
import time
from rpi_ws281x import *
import argparse

# Led configurations
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

PIN_NUM        = 15

def clearStrip(strip):
    strip.setPixelColor(PIN_NUM, Color(0,0,0))
    strip.show()
    # for i in range(strip.numPixels()):
    #     strip.setPixelColor(i, Color(0,0,0))
    #     strip.show()

def red(strip):
    strip.setPixelColor(PIN_NUM, Color(255,0,0))
    strip.show()
    # for i in range(strip.numPixels()):
    #     strip.setPixelColor(i, Color(255,0,0))
    #     strip.show()

def yellow(strip):
    strip.setPixelColor(PIN_NUM, Color(0,255,0))
    strip.show()
    # for i in range(strip.numPixels()):
    #     strip.setPixelColor(i, Color(0,255,0))
    #     strip.show()

def blue(strip):
    strip.setPixelColor(PIN_NUM, Color(0,0,255))
    strip.show()
    # for i in range(strip.numPixels()):
    #     strip.setPixelColor(i, Color(0,0,255))
    #     strip.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    try:
        while True:
            c = input("Choose color (r, y, b):\n")
            if c is 'r':
                red(strip)
                print("Color is now red!")
            elif c is 'y':
                yellow(strip)
                print("Color is now yellow!")
            elif c is 'b':
                blue(strip)
                print("Color is now blue!")
            else:
                print("Give valid input (r, y, b)")
    except KeyboardInterrupt:
        clearStrip(strip)
        print("")
