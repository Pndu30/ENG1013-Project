"""
Polling Loop function file
Last edited by: Pandu Raditya Rohman
Version: 3
Last modified: 13/10/2023
"""

import time
import math
import sevseg
thermIn = 0
lightIn = 1
serialPinOutputs = 6
rclckPinOutputs = 5
srclckPinOutputs = 4
alertPin = 3
sleepTime = 0.5
risePin = 16
fallPin = 17

def get_temp(dataset, board,thermIn=thermIn):
    """
    Function that gets the voltage from the thermistor through an analog input
    and converts it to temperature data.

    Args:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
        board: The Arduino
        thermIn (Integer): Analog pin number for the thermistor

    Returns:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
    """
    voltOut = (board.analog_read(thermIn)[0])*(5/1023)
    if voltOut > 0:
        thermRes = ((voltOut*10)/5)/(1-(voltOut/5))
        dataset[0] = round(83.966601613537950*math.exp(-0.116185042196742*thermRes))
        if len(dataset[1]) != 20:
            dataset[1].append(dataset[0])
        else:
            dataset[1].pop(0)
            dataset[1].append(dataset[0])
        
        if len(dataset[1])>=2 and len(dataset[5])>=2:
            lastTemp1 = dataset[1][-1]
            lastTemp2 = dataset[1][-2]
            lastTime1 = dataset[5][-1]
            lastTime2 = dataset[5][-2]
            grad = (lastTemp1-lastTemp2)/(lastTime1-lastTime2)
            if len(dataset[2]) <= 20:
                dataset[2].append(grad)
            else:
                dataset[2].pop(0)
                dataset[2].append(grad)
                
    return dataset

def get_light(dataset, board, lightIn=lightIn):
    """
    Function that gets the voltage from the LDR through an analog input
    and converts it to lux data.

    Args:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
        board: The Arduino
        lightIn (Integer): Analog pin number for the LDR

    Returns:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
    """
    voltOut = (board.analog_read(lightIn)[0])*(5/1023)
    if voltOut > 0:
        ldrRes = ((voltOut*10)/5)/(1-(voltOut/5))
        dataset[3] = 1560.31496068566*math.exp(-0.0006516603208904828*ldrRes)
        if len(dataset[4]) != 20:
            dataset[4].append(dataset[3])
        else:
            dataset[4].pop(0)
            dataset[4].append(dataset[0])
    return dataset


def rapid_changing_temp_check(gradData):
    """
    Function that checks if there's a rapid change in temperature

    Args:
        gradData (List): The data storing the gradient/change in temperature

    Returns:
        Boolean: True if there's a rapid change, False if there's none
    """
    if len(gradData) < 2:
        return False
    else:
        if ((gradData[-1]-3)>gradData[-2]) or ((gradData[-1]+3)<gradData[-2]):
            return True
        else:
            return False


def rapid_changing_temp(gradData,duration,board,risePin=risePin,fallPin=fallPin,alertPin=alertPin):
    """
    Function that generates an output when ther's a rapid change in temperature

    Args:
        gradData (List): The data storing the gradient/change in temperature
        duration (Integer): The time the output is being outputted
        board: The Arduino
        risePin (Integer): Digital pin number for the output when the temperature rises quickly.
        fallPin (Integer): Digital pin number for the output when the temperature rises quickly.
    """
    if len(gradData) < 2:
        return False
    else:        
        try:
            board.digital_pin_write(alertPin,1)
            if ((gradData[-1]-3)>gradData[-2]):
                board.digital_pin_write(risePin,1)
                print(f"Change in temperature too high, with change of {gradData[-1]}")
                sevseg.write_sevseg("Rapid rise",1,board)
                time.sleep(duration)
                board.digital_pin_write(risePin,0)
            elif ((gradData[-1]+3)<gradData[-2]):
                board.digital_pin_write(fallPin,1)
                print(f"Change in temperature too high, with change of {gradData[-1]}")
                sevseg.write_sevseg("Rapid fall",1,board)
                time.sleep(duration)
                board.digital_pin_write(fallPin,0)
            board.digital_pin_write(alertPin,0)
        except KeyboardInterrupt:
            pass

def light_check(currentLight,fanSpeed):
    """
    Function that checks the lux being inputted.

    Args:
        currentLight (Integer): The current lux being received by the LDR
        fanSpeed (Integer): The speed of the fan.

    Returns:
        fanSpeed (Integer): The speed of the fan being set by the system
    """
    if currentLight>1000:
        fanSpeed = 2
    else:
        fanSpeed = 1
    return fanSpeed

def thermometer_check(currentTemp,maxTemp,minTemp):
    """
    Function that checks the temperature and gives an output of the appropriate thermometer output

    Args:
        currentTemp (Integer): The current temperature being received by the thermistor
        maxTemp (Integer): The upper bound of the temperature's limit set
        minTemp (Integer): The lower bound of the temperature's limit set

    Returns:
        type (string): String indicating the temperature for the thermometer
    """
    types = ['tooHot','Hot','notVeryHot','neutral3','neutral2','neutral1','tooCold','cold','notVeryCold']
    if currentTemp > maxTemp:
        if currentTemp > (maxTemp + 10):
            return types[0]
        elif currentTemp > (maxTemp+5):
            return types[1]
        else:
            return types[2]
    elif currentTemp < minTemp:
        if currentTemp < (minTemp-10):
            return types[6]
        elif currentTemp < (minTemp-5):
            return types[7]
        else:
            return types[8]
    else:
        if currentTemp > ((maxTemp+minTemp)/2):
            return types[3]
        elif currentTemp < ((maxTemp+minTemp)/2):
            return types[5]
        else:
            return types[4]


def outputs(currentTemp,gradData,currentLight,settings,board,serialPin=serialPinOutputs,rclckPin=rclckPinOutputs,srclckPin=srclckPinOutputs,alertPin=alertPin):
    """
    The main outputs function, which outputs depending on the conditions given

    Args:
        currentTemp (Integer): The current temperature being received by the thermistor
        gradData (List): The data storing the gradient/change in temperature
        currentLight (Integer): The current lux being received by the LDR
        settings (List): List of the settings set by the user. This consists of the upper and lower bound of the temperature and fan speed
        board: The Arduino
        serialPin (Integer): Digital pin number for the shift register's serial pin.
        rclckPin (Integer): Digital pin number for the shift register's register clock pin.
        srclckPin (Integer): Digital pin number for the shift register's serial clock pin.
        alertPin (Integer): Digital pin number for if there's a rapid change in temperature.
    """
    ledDict = {
        # Using 2 shift registers
        # For normal outputs 3 Red 3 Green 3 Blue convention
        'cold1TooHot': '0111100000000001',
        'cold1Hot': '0101100000000001',
        'cold1NotVeryHot': '0100100000000001',
        'cold2TooHot': '1111100000000011',
        'cold2Hot': '1101100000000011',
        'cold2NotVeryHot': '1100100000000011',
        'heat1TooCold': '0100000011101000',
        'heat1Cold': '0100000001101000',
        'heat1NotVeryCold': '01000000001001000',
        'heat2TooCold': '1100000011111000',
        'heat2Cold': '1100000001111000',
        'heat2NotVeryCold': '1100000000111000',        
        'neutral3': '0000011100000000',
        'neutral2': '0000001100000000',
        'neutral1': '0000000100000000',
        'change': '0000000000010000',
        'reset': '0000000000000000'
    }
    lowBound = settings[0]
    upBound = settings[1]
    ventSpeed = settings[2]
    
    for serial in ledDict['reset']:
        board.digital_pin_write(serialPin,int(serial))
        board.digital_pin_write(srclckPin,1)
        time.sleep(0.0001)
        board.digital_pin_write(srclckPin,0)
    board.digital_pin_write(rclckPin,1)
    time.sleep(0.0001)
    board.digital_pin_write(rclckPin,0)
    board.digital_pin_write(alertPin,0)
    sevseg.write_sevseg('    ',0.001,board)

    if rapid_changing_temp_check(gradData):
        rapid_changing_temp(gradData,1,board)
        for serial in ledDict['change']:
            board.digital_pin_write(serialPin,int(serial))
            board.digital_pin_write(srclckPin,1)
            time.sleep(0.0001)
            board.digital_pin_write(srclckPin,0)
        board.digital_pin_write(rclckPin,1)
        time.sleep(0.0001)
        board.digital_pin_write(rclckPin,0)
        
        
    ventSpeed = light_check(currentLight,ventSpeed)
    thermometer_val = thermometer_check(currentTemp,upBound,lowBound)
        
    if currentTemp < lowBound:
        if ventSpeed == 2:
            if thermometer_val == 'tooCold':
                for serial in ledDict['heat2TooCold']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too cold ({currentTemp}), heating up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
            elif thermometer_val == 'cold':
                for serial in ledDict['heat2Cold']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too cold ({currentTemp}), heating up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
            else:
                for serial in ledDict['heat2NotVeryCold']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too cold ({currentTemp}), heating up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
        else:
            if thermometer_val == 'tooCold':
                for serial in ledDict['heat1TooColc']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too cold ({currentTemp}), heating up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
            elif thermometer_val == 'cold':
                for serial in ledDict['heat1Cold']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too cold ({currentTemp}), heating up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
            else:
                for serial in ledDict['heat1NotVeryCold']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too cold ({currentTemp}), heating up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
    
    elif currentTemp > upBound:
        if ventSpeed == 2:
            if thermometer_val == 'tooHot':
                for serial in ledDict['cold2TooHot']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too hot ({currentTemp}), cooling down with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
            elif thermometer_val == 'hot':
                for serial in ledDict['cold2Cold']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too hot ({currentTemp}), cooling down with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
            else:
                for serial in ledDict['cold2NotVeryHot']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too hot ({currentTemp}), cooling down with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
        else:
            if thermometer_val == 'tooHot':
                for serial in ledDict['cold1TooHot']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too hot ({currentTemp}), cooling down up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
            elif thermometer_val == 'hot':
                for serial in ledDict['cold1hot']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too hot ({currentTemp}), cooling down up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
            else:
                for serial in ledDict['cold1NotVeryHot']:
                    board.digital_pin_write(serialPin,int(serial))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(rclckPin,0)
                print(f"Temperature too hot ({currentTemp}), cooling down up with vent speed {ventSpeed}")
                msg = str(currentTemp)+'*c'
                sevseg.write_sevseg(msg,2.5,board)
    
    else:
        if thermometer_val == 'neutral3':
            for serial in ledDict['neutral3']:
                board.digital_pin_write(serialPin,int(serial))
                board.digital_pin_write(srclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(srclckPin,0)
            board.digital_pin_write(rclckPin,1)
            time.sleep(0.0001)
            board.digital_pin_write(rclckPin,0)
            print(f"Temperature is within the goal range ({currentTemp})")
            msg = str(currentTemp)+'*c'
            sevseg.write_sevseg(msg,2.5,board)
        elif thermometer_val == 'neutral2':
            for serial in ledDict['neutral2']:
                board.digital_pin_write(serialPin,int(serial))
                board.digital_pin_write(srclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(srclckPin,0)
            board.digital_pin_write(rclckPin,1)
            time.sleep(0.0001)
            board.digital_pin_write(rclckPin,0)
            print(f"Temperature is within the goal range ({currentTemp})")
            msg = str(currentTemp)+'*c'
            sevseg.write_sevseg(msg,2.5,board)
        else:
            for serial in ledDict['neutral1']:
                board.digital_pin_write(serialPin,int(serial))
                board.digital_pin_write(srclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(srclckPin,0)
            board.digital_pin_write(rclckPin,1)
            time.sleep(0.0001)
            board.digital_pin_write(rclckPin,0)
            print(f"Temperature is within the goal range ({currentTemp})")
            msg = str(currentTemp)+'*c'
            sevseg.write_sevseg(msg,2.5,board)


def polling_loop(dataset,settings,board,serialPin=serialPinOutputs,rclckPin=rclckPinOutputs,srclckPin=srclckPinOutputs):
    """
    The main polling loop function for the system.

    Args:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
        settings (List): List of the settings set by the user. This consists of the upper and lower bound of the temperature and fan speed
        board: The Arduino
        serialPin (Integer): Digital pin number for the shift register's serial pin.
        rclckPin (Integer): Digital pin number for the shift register's register clock pin.
        srclckPin (Integer): Digital pin number for the shift register's serial clock pin.  
    
    Returns:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
        """
    timeData = dataset[5]
    while True:
        try:
            start = time.time()
            dataset = get_temp(dataset,board)
            dataset = get_light(dataset,board)
            outputs(dataset[0],dataset[2],dataset[3],settings,board)
            stop = time.time()
            if len(timeData)<20:
                timeData.append(timeData[-1] + (stop-start))
            else:
                timeData.pop(0)
                timeData.append(timeData[-1] + (stop-start))
            print(f"Light intensity: {round(dataset[3],2)} lux")
            print(f"Time taken: {round(time.time()-start,2)} s")
            print("Ctrl + C to stop")
            time.sleep(0.005)
        except KeyboardInterrupt:
            for i in range(16):
                board.digital_pin_write(serialPin,0)
                board.digital_pin_write(srclckPin,1)
                time.sleep(0.0001)
                board.digital_pin_write(srclckPin,0)
            board.digital_pin_write(rclckPin,1)
            time.sleep(0.0001)
            board.digital_pin_write(rclckPin,0)
            sevseg.write_sevseg('    ',0.01,board)
            return dataset