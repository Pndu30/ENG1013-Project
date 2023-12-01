"""
PIN fucntion file
Last edited by: Pandu Raditya Rohman
Version: 1
Last modified: 11/09/2023
"""

import time

def set_pin():
    """
    Function that sets a pin for the user at.
    
    Return:
        pin (Integer): Variable containing pin
    """
    while True:
        try:
            pin = int(input("Please input a 4-digit number as a pin: "))
            if len(str(pin))>4:
                print("Please only put in 4 digits")
            else:
                break
        except ValueError:
            print("Please only input numbers")
    return pin

def check_pin(pin):
    """
    Function that asks the user and checks the pin. Failure results in a 2 minute timeout.
    
    Parameter:
        pin (Integer): Variable containing pin
    """
    i = 0    
    while i!=3:
        while True:
            try:
                pinInput = int(input("Please enter the pin: "))
                if len(str(pinInput))!=4:
                    print("Please only put in 4 digits")
                else:
                    break 
            except ValueError:
                print("Please only enter integers")
            
        if pinInput == pin:
            print("Correct")
            break
        else:
            i+=1
            if i == 3:
                print("You're locked out for some time")
                counter = 0
                startCount = time.time()
                while True:
                    try:
                        if counter<120:
                            endCount = time.time()
                            counter = endCount - startCount
                        else:
                            break
                    except KeyboardInterrupt:
                        print(f"Still in lockout mode for {120-counter} more seconds")
                break
            else:
                print(f"Wrong pin, please try again. You have {3-i} tries left")
