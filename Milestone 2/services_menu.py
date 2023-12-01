"""
Services Subsystem function file
Created by: Pandu Raditya Rohman
Version: 1
Last modified: 11/09/2023
"""
import matplotlib.pyplot as plt
import math
import time
import temp_pin_func as tpf
import sevseg
import Polling_Loop as ploop

def main_menu():
    """
    Function that shows the main menu.

    Return:
        option (Integer): The menu option which the user picks
        'quit: For KeyboardInterrupt error so the program can terminate smoothly
    """
    while True:
        try:
            print("\n1. Turn on/off")
            print("2. Maintenance mode")
            print("3. Data obsevation")
            print("Ctrl+C to terminate the program")
            print("--------------------")
            option = int(input("Please pick one of the option: "))
                
            if option>0 and option<=3:
                return option
                break
            else:
                print("Please only input from the menu available\n")
        except ValueError:
            print("Please only input from the menu available\n")
        except KeyboardInterrupt:
            print("\nTerminating program")
            return 'quit'
        
def turn_on_off(tempData,tempLow,tempHigh,ventSpeed,board):
    """
    Function that shows the first part of the services subsystem.
    Place to turn the system on.

    Parameters:
        tempData (List): List that stores the data taken
        tempLow (Integer): The lower boundary of the temperature range
        tempHigh (Integer): The upper boundary of the temperature range
        ventSpeed (Integer): The speed of ventilation (Either 1 or 2)
        board: The Arduino
    """
    while True:
            try:
                print("1. Turn on system")
                print("2. Turn off system")
                print("Ctrl + C to return to main menu")
                print("--------------------")
                turnOnOffChoice = int(input("Please pick one of the option: "))
                    
                if turnOnOffChoice > 0 and turnOnOffChoice <= 2:
                    if turnOnOffChoice == 1:
                         ploop.polling_loop(tempData,tempLow,tempHigh,ventSpeed,board)
                    elif turnOnOffChoice == 2:
                        continue
                else:
                    print("Please only input from the menu available\n")
                    continue
                    
            except ValueError:
                print("Please only input from the menu available\n")
            except KeyboardInterrupt:
                break
    
def maintenance(pin, tempLow, tempHigh, ventSpeed,board):
    """
    Function that shows the maintenance part of the services subsystem.

    Parameters:
        pin (Integer): Variable containing pin
        tempLow (Integer): The lower boundary of the temperature range
        tempHigh (Integer): The upper boundary of the temperature range
        ventSpeed (Integer): The speed of ventilation (Either 1 or 2)
        board: The Arduino

    Return (as a list):
        tempLow (Integer): The lower boundary of the temperature range
        tempHigh (Integer): The upper boundary of the temperature range
        ventSpeed (Integer): The speed of ventilation (Either 1 or 2)
    """
    tpf.check_pin(pin)
    sevseg.write_sevseg('0000',board)
    while True:
        try:
            print(f"Current temperature range is between {tempLow} and {tempHigh}")
            print(f"Current ventilation speed: {ventSpeed}\n")
            print("--------------------------")
            print("What would you like to do")
            print("1. Change the temperature range")
            print("2. Change the ventilation speed")
            print("Ctrl + C to return to main menu")
            print("-----------------------")
            maintenanceOpt = int(input("Please pick one of the option: "))

            if maintenanceOpt == 1:
                while True:
                    try:
                        print("Please only input values between 5 and 30") 
                        print("Ctrl + C to return to main menu")
                        print("-----------------------")
                        tempLow = int(input("Input new low temp: "))
                        tempHigh = int(input("Input new high temp: "))
                        if tempLow>5 and tempHigh<30:
                            return [tempLow, tempHigh, ventSpeed]
                        else:
                            print("Please only input values between 5 and 30")
                    except ValueError:
                        print("Please only input numbers")
                    except KeyboardInterrupt:
                        break
            elif maintenanceOpt == 2:
                while True:
                    try:
                        print("Please only input 1 or 2")
                        print("1 for low")
                        print("2 for high")
                        print("Ctrl + C to return to main menu")
                        print("-----------------------")
                        ventSpeed = int(input("Input new vent speed: "))
                        if (ventSpeed == 1) or (ventSpeed == 2):
                            return [tempLow, tempHigh, ventSpeed]
                        else:
                            print("Please only input 1 or 2")
                    except ValueError:
                        print("Please only input numbers")
                    except KeyboardInterrupt:
                        break
                    
            else:
                print("Please only input from the menu available\n")
                continue
            
            break
        except ValueError:
            print("Please only input from the menu available\n")
        except KeyboardInterrupt:
            break
    

def data_observation(tempData, timeData):
    """
    Function that shows the data observation part of the services subsystem.

    Parameters:
        tempData (List): List that stores the data taken
        timeData (List): Local variable that shows the time for the graph
    """
    while True:
        try:
            print("\nIn data observation mode")
            print("Ctrl+C to return to main menu")
            print("--------------------")

            dataOpt = input("Get graph(y/n): ").lower()
            
            if dataOpt == 'y':
                if len(tempData)==20:
                    timeData = []
                    for i in range(len(tempData)):
                        timeData.append(i)
                    plt.plot(timeData, tempData)
                    plt.title("Temperature vs Time")
                    plt.xlabel("Time (s)")
                    plt.ylabel("Temperature (C)")
                    plt.axes([0,30,0,100])
                    plt.show()
                else:
                    print("Not enough data to plot")
        except KeyboardInterrupt:
            break

