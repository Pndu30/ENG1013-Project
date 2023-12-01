"""
Polling Loop function file
Created by: Pandu Raditya Rohman
Version: 1
Last modified: 11/09/2023
"""
import time
import math
import sevseg
thermIn = 0
redPin = [15,16]
bluePin = [17,18]
allLedPins = redPin + bluePin
sleepTime = 0.8

def get_temp(tempData, board,thermIn=thermIn):
    """
    Function that gets the voltage from the thermistor through an analog input
    and converts it to temperature data.
    
    Parameters:
        tempData (List): List that stores the data taken
        board: The Arduino
        thermIn: Analog pin for the thermistor

    Return (as a list):
        temp (float): The converted value from the voltage received
        tempData (List): List that stores the data taken 
    """
    voltOut = (board.analog_read(thermIn)[0])*(5/1023)
    temp = 0
    if voltOut > 0:
        thermRes = ((voltOut*10)/5)/(1-(voltOut/5))
        temp = -(21.21*math.log(thermRes)) + 72.203
        if len(tempData) != 20:
            tempData.append(temp)
        else:
            tempData.pop(0)
            tempData.append(temp)
    return [temp, tempData]
    

def outputs(currentTemp,tempLow,tempHigh,ventSpeed,board,redPin=redPin,bluePin=bluePin,allLedPins=allLedPins):
    """
    Function that gives an output (Turn on/off specific LEDs) depending on the current temperature input.

    Parameters:
        currentTemp (Integer): The latest temperature data received from get_temp
        tempLow (Integer): The lower boundary of the temperature range
        tempHigh (Integer): The upper boundary of the temperature range
        ventSpeed (Integer): The speed of ventilation (Either 1 or 2)
        board: The Arduino
        redPin: Number of pins connected to the red LEDs
        bluePin: Number of pins connected to the blue LEDs
        allLedPins: List containing number of pins for both blue and red LEDs
    """
    for pin in allLedPins:
            board.digital_pin_write(pin,0)
            time.sleep(sleepTime)
    sevseg.write_sevseg('    ',board)

    if currentTemp < tempLow:
        if ventSpeed == 2:
            for pin in redPin:
                board.digital_pin_write(pin,1)
            print(f"Temperature too cold ({currentTemp}), heating up with vent speed {ventSpeed}")
            print("Ctrl + C to stop")
            msg = str(currentTemp)+'*c'
            start = time.time()
            counter = 0
            while counter<1.34:
                end = time.time()
                sevseg.write_sevseg(msg,board)
                counter = end-start
        else:
            board.digital_pin_write(redPin[0],1)
            print(f"Temperature too cold ({currentTemp}), heating up with vent speed {ventSpeed}")
            print("Ctrl + C to stop")
            msg = str(currentTemp)+'*c'
            start = time.time()
            counter = 0
            while counter<1.34:
                end = time.time()
                sevseg.write_sevseg(msg,board)
                counter = end-start
    elif currentTemp > tempHigh:
        if ventSpeed == 2:
            for pin in bluePin:
                board.digital_pin_write(pin,1)
            print(f"Temperature too hot ({currentTemp}), cooling down with vent speed {ventSpeed}")
            print("Ctrl + C to stop")
            msg = str(currentTemp)+'*c'
            start = time.time()
            counter = 0
            while counter<1.34:
                end = time.time()
                sevseg.write_sevseg(msg,board)
                counter = end-start
        else:
            board.digital_pin_write(bluePin[0],1)
            print(f"Temperature too hot ({currentTemp}), cooling down with vent speed {ventSpeed}")
            print("Ctrl + C to stop")
            msg = str(currentTemp)+'*c'
            start = time.time()
            counter = 0
            while counter<1.34:
                end = time.time()
                sevseg.write_sevseg(msg,board)
                counter = end-start
    else:
        print(f"Temperature is within the goal range ({currentTemp})")
        print("Ctrl + C to stop")
        msg = str(round(currentTemp))+'*c'
        start = time.time()
        counter = 0
        while counter<1.34:
            end = time.time()
            sevseg.write_sevseg(msg,board)
            counter = end-start
    time.sleep(sleepTime)
    
def polling_loop(tempData,tempLow,tempHigh,ventSpeed,board,allLedPins=allLedPins):
    """
    Polling loop function for the system.
    
    Parameters:
        tempData (List): List that stores the data taken
        tempLow (Integer): The lower boundary of the temperature range
        tempHigh (Integer): The upper boundary of the temperature range
        ventSpeed (Integer): The speed of ventilation (Either 1 or 2)
        board: The Arduino
    """
    while True:
        try:
            currentTemp = round(get_temp(tempData,board)[0])
            time.sleep(0.05)
            outputs(currentTemp,tempLow,tempHigh,ventSpeed,board)
            time.sleep(0.05)
        except KeyboardInterrupt:
            for pin in allLedPins:
                board.digital_pin_write(pin,0)
            break