"""
Main HVAC file
Last edited by: Pandu Raditya Rohman
Version: 2
Last modified: 13/10/2023
"""
# Importing main modules
import math
import time
from pymata4 import pymata4
import matplotlib

# Defining board and pins
board = pymata4.Pymata4()
digitalPins = [3,4,5,6,7,8,9,10,11,12,13,16,17]
analogPins = [0,1]

for pin in digitalPins:
    board.set_pin_mode_digital_output(pin)
for pin in analogPins:
    board.set_pin_mode_analog_input(pin)
    
# Set up initial variables
tempHigh = 20
tempLow = 18
currentTemp = 0
ventSpeed = 1
currentLight = 0
tempData = []
gradData = []
lightData = []
timeData = [0]
dataset = [currentTemp,tempData,gradData,currentLight,lightData,timeData]
settings = [tempLow, tempHigh, ventSpeed]

# Importing self made modules
import temp_pin_func as tpf
import sevseg
import Polling_Loop as ploop
import services_menu as serv

# Run the program
pin = tpf.set_pin()
while True:
    try:
        menu = serv.main_menu()
        if menu == 1:
            dataset = serv.turn_on_off(dataset,settings,board)
        elif menu == 2:
            settings = serv.maintenance(pin,settings,board)
        elif menu == 3:
            serv.data_observation(dataset)
        elif menu == 4:
            print("\nTerminating program...")
            break
    except KeyboardInterrupt:
        pass
board.shutdown()