"""
Services Subsystem function file
Last edited by: Pandu Raditya Rohman
Version: 3
Last modified: 13/10/2023
"""

import matplotlib.pyplot as plt
import math
import time
import temp_pin_func as tpf
import sevseg
import Polling_Loop as ploop
timeLimit = 60

def main_menu():
    """
    The function that shows the main menu

    Returns:
        option (Integer): The menu option which the user picks
    """
    while True:
        try:
            # Shows the main menu
            print("\n1. Turn on/off")
            print("2. Maintenance mode")
            print("3. Data obsevation")
            print("4. Terminate the program")
            print("--------------------")
            option = int(input("Please pick one of the option: "))
                
            # Check if input is valid
            if option>0 and option<=4:
                return option
            else:
                print("Please only input from the menu available\n")
        except ValueError:
            print("Please only input from the menu available\n")
        except KeyboardInterrupt:
            print("\nPlease only input from the menu available\n")
        
def turn_on_off(dataset,settings,board):
    """
    Function that shows the first part of the services subsystem.
    Place to turn the system on.

    Args:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
        settings (List): List of the settings set by the user. This consists of the upper and lower bound of the temperature and fan speed
        board: The Arduino
        
    Returns:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
    """
    while True:
            try:
                # Shows the main menu
                print("1. Turn on system")
                print("2. Turn off system")
                print("Ctrl + C to return to main menu")
                print("--------------------")
                turnOnOffChoice = int(input("Please pick one of the option: "))
                    
                # Check if input is valid
                if turnOnOffChoice > 0 and turnOnOffChoice <= 2:
                    if turnOnOffChoice == 1:
                        dataset = ploop.polling_loop(dataset,settings,board)
                    elif turnOnOffChoice == 2:
                        continue
                else:
                    print("Please only input from the menu available\n")
                    continue
                    
            except ValueError:
                print("Please only input from the menu available\n")
            except KeyboardInterrupt:
                return dataset
    
def maintenance(pin, settings, board, timeLimit=timeLimit):
    """
    Function that shows the maintenance part of the services subsystem.

    Args:
        pin (Integer): Variable containing pin
        settings (List): List of the settings set by the user. This consists of the upper and lower bound of the temperature and fan speed
        board: The Arduino
        timeLimit (Integer): The time limit for how long the user can stay. Defaults to timeLimit.
        
    Returns:
        settings (List): List of the settings set by the user. This consists of the upper and lower bound of the temperature and fan speed
    """
    # Ask for pin
    tpf.check_pin(pin)    
    lowBoundOld = settings[0]
    upBoundOld = settings [1]
    ventSpeedOld = settings[2]
    
    while True:
        try:
            # Show the options
            print(f"Current temperature range is between {lowBoundOld} and {upBoundOld}")
            print(f"Current ventilation speed: {ventSpeedOld}")
            print("--------------------------")
            print("What would you like to do")
            print("1. Change the temperature range")
            print("2. Change the ventilation speed")
            print("Ctrl + C to return to main menu")
            print("-----------------------")
            start = time.time()
            maintenanceOpt = int(input("Please pick one of the option: "))
            end = time.time()
            
            # Checks if the user is still within the limit
            if end-start>timeLimit:
                print("Took too long to answer, please login again")
                return [lowBoundOld,upBoundOld,ventSpeedOld]
            
            # Temperature options
            elif maintenanceOpt == 1:
                while True:
                    try:
                        # Show the options
                        print("Please only input values between 5 and 30") 
                        print("Ctrl + C to return to main menu")
                        print("-----------------------")
                        start = time.time()
                        lowBoundNew = int(input("Input new low temp: "))
                        upBoundNew = int(input("Input new high temp: "))
                        
                        # Checks if the user is still within the limit
                        end = time.time()
                        if end-start>timeLimit:
                            print("Took too long to answer, please login again")
                            return [lowBoundOld,upBoundOld,ventSpeedOld]
                        elif lowBoundNew>upBoundNew:
                            print("Upper and Lower bound might have been mismatched, please try again")
                        elif (lowBoundNew<=5) and (upBoundNew>=30):
                            print("Please only input values between 5 and 30")
                        else:
                            return [lowBoundNew,upBoundNew,ventSpeedOld]
                    except ValueError:
                        print("Please only input numbers")
                    except KeyboardInterrupt:
                        return [lowBoundOld,upBoundOld,ventSpeedOld]
            
            # Fanspeed options
            elif maintenanceOpt == 2:
                while True:
                    try:
                        # Show the options
                        print("Please only input 1 or 2")
                        print("1 for low")
                        print("2 for high")
                        print("Ctrl + C to return to main menu")
                        print("-----------------------")
                        start = time.time()
                        ventSpeedNew = int(input("Input new vent speed: "))
                        end = time.time()
                        
                        # Checks if the user is still within the limit
                        if end-start>timeLimit:
                            print("Took too long to answer, please login again")
                            return [lowBoundOld,upBoundOld,ventSpeedOld] 
                        elif (settings[2] == 1) or (settings[2] == 2):
                            return [lowBoundOld,upBoundOld,ventSpeedNew]
                        else:
                            print("Please only input 1 or 2")
                    except ValueError:
                        print("Please only input numbers")
                    except KeyboardInterrupt:
                        return [lowBoundOld,upBoundOld,ventSpeedOld]
                    
            else:
                print("Please only input from the menu available\n")
                continue
            
        except ValueError:
            print("Please only input from the menu available\n")
        except KeyboardInterrupt:
            return [lowBoundOld,upBoundOld,ventSpeedOld]
    
def data_observation(dataset):
    """
    Function that shows the data observation part of the services subsystem.

    Args:
        dataset (List): List of data needed consisting of temperature, light, change in temperature, and time
    """
    # Get the data from the dataset
    tempData = dataset[1]
    gradData = dataset[2]
    lightData = dataset[4]
    timeData = dataset[5]
    
    while True:
        try:
            # Show the options
            print("\nIn data observation mode")
            print("1. Temperature graph")
            print("2. Change in temperature graph")
            print("3. Light graph")
            print("Ctrl+C to return to main menu")
            print("--------------------")

            dataOpt = int(input("Please pick one of the option: "))
            saveOpt = input("Do you want to save the data(y/n): ")
            # Graphing
            if dataOpt == 1:
                if len(tempData) < 20:
                    print("Not enough data to plot")
                    print(len(tempData))
                elif saveOpt == 'y':
                    plt.plot(timeData, tempData)
                    plt.title("Temperature vs Time")
                    plt.xlabel("Time (s)")
                    plt.ylabel("Temperature (C)")
                    name = time.strftime("%d%m%Y%H%M%S", time.localtime()) + " TemperatureData.png"
                    plt.savefig(str(name))
                    plt.show()
                else:
                    plt.plot(timeData, tempData)
                    plt.title("Temperature vs Time")
                    plt.xlabel("Time (s)")
                    plt.ylabel("Temperature (C)")
                    plt.show()
            elif dataOpt == 2:
                if len(gradData) < 10:
                    print("Not enough data to plot")
                elif saveOpt == 'y':
                    plt.plot(timeData[0:9], gradData[0:9])
                    plt.title("Change in Temperature vs Time")
                    plt.xlabel("Time (s)")
                    plt.ylabel("Change in temperature (C)")
                    name = time.strftime("%d%m%Y%H%M%S", time.localtime()) + "ChangeInTemperatureData.png"
                    plt.savefig(str(name))
                    plt.show()
                else:
                    plt.plot(timeData[0:9], gradData[0:9])
                    plt.title("Change in Temperature vs Time")
                    plt.xlabel("Time (s)")
                    plt.ylabel("Change in temperature (C)")
                    plt.show()
            elif dataOpt == 3:
                if len(lightData)<20:
                    print("Not enough data to plot")
                elif saveOpt == 'y':
                    plt.plot(timeData, lightData)
                    plt.title("Light Intensity vs Time")
                    plt.xlabel("Time (s)")
                    plt.ylabel("Light Intensity (Lux)")
                    name = time.strftime("%d%m%Y%H%M%S", time.localtime()) + " LightData.png"
                    plt.savefig(str(name))
                    plt.show()
                else:
                    plt.plot(timeData, lightData)
                    plt.title("Light Intensity vs Time")
                    plt.xlabel("Time (s)")
                    plt.ylabel("Light Intensity (Lux)")
                    plt.show()
            else:
                print("Please only input whole numbers between 1 and 3")
        except KeyboardInterrupt:
            break
        except ValueError:
            print("Please only input whole numbers between 1 and 3")

