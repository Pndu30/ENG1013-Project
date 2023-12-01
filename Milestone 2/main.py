"""
Main HVAC file
Created by: Pandu Raditya Rohman
Version: 1
Last modified: 11/09/2023
"""
# Main modules
import math
import time
from pymata4 import pymata4
import matplotlib

# Define board
board = pymata4.Pymata4()
# define pins used by segments
thermIn = 0
segPins = [3,4,5,6,7,8,9]
onPins = [10,11,12,13]
redPin = [15,16]
bluePin = [17,18]
allLedPins = redPin + bluePin
allsevsegPins = segPins + onPins
allPins = allLedPins + allsevsegPins

# Set up initial variables
tempHigh = 20
tempLow = 18
currentTemp = 0
ventSpeed = 1
tempData = []
timeData = []
lock = 0

# Self made modules
import temp_pin_func as tpf
import sevseg
import Polling_Loop as ploop
import services_menu as serv

# set up pins for digital output
for pin in allPins:
    board.set_pin_mode_digital_output(pin)
# Set up pins for analog input
board.set_pin_mode_analog_input(thermIn,callback=ploop.get_temp(tempData,board))

# Run the program
pin = tpf.set_pin()
while True:
    try:
        menu = serv.main_menu()
        if menu == 1:
            serv.turn_on_off(tempData,tempLow,tempHigh,ventSpeed,board)
        elif menu == 2:
            outs = serv.maintenance(pin,tempLow,tempHigh,ventSpeed,board)
            tempLow = outs[0]
            tempHigh = outs[1]
            ventSpeed = outs[2]
        elif menu == 3:
            serv.data_observation(tempData,timeData)
        elif menu == 'quit':
            print("\nTerminating program...")
            break
    except KeyboardInterrupt:
        break
board.shutdown()