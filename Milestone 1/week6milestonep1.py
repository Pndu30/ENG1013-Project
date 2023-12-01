def get_temp():
    print("Get input")
    return 20
    
def turn_on_fan():
    print("Fan on, heater off")

def turn_on_heater():
    print("Heater on, fan off")

def turn_off_both():
    print("Fan and heater off, temperature within range")

def main_menu():
    while True:
        try:
            print("\nIn main menu")
            print("1. Turn system on/off")
            print("2. Maintenance mode")
            print("3. Data obsevation")
            print("Ctrl+C to terminate the program")
            print("--------------------")
            option = int(input("Please pick one of the option: "))
            if option>0 and option<=3:
                return option
                break
            else:
                print("\nPlease only input from the menu available\n")
        except ValueError:
                print("\nPlease only input from the menu available\n")
        except KeyboardInterrupt:
            print("\nTerminating program...")
            return 4

def normal_mode():
    while True:
        try:
            print("\nIn normal mode")
            print("Ctrl+C to return to main menu")
            print("--------------------")
            exit = input("Do you want to turn on the system(y/n): ").lower()
            
            if exit == 'y':
                exit = 0
                polling_loop(exit,lowTemp,topTemp)
            elif exit == 'n':
                continue
            else:
                print("Please only input (y/n)\n")
        except KeyboardInterrupt:
            return 4
            
def maintenance_mode():
    while True:
        try:
            print("\nIn maintenance mode mode")
            print("Ctrl+C to return to main menu")
            print("--------------------")

            opt = input("Do you want to change the temperature range(y/n): ").lower()
            
            if opt == 'y':
                print("Change temp range here")
                print("Ctrl+C to return to main menu")
                print("--------------------")
                tempLow = input("Input new low temp: ")
                tempHigh = input("Input new high temp: ") 
            elif opt == 'n':
                continue
            else:
                print("Please only answer with y/n")
        except KeyboardInterrupt:
            return 4
        
    
def data_obsv_mode():
    while True:
        try:
            print("\nIn data observation mode")
            print("Ctrl+C to return to main menu")
            print("--------------------")

            opt = input("Get graph(y/n): ").lower()
            
            if opt == 'y':
                print("Show graph here")
            elif opt == 'n':
                continue
            else:
                print("Please only answer with y/n")
        except KeyboardInterrupt:
            return 4
                

def polling_loop(exit,topTemp,lowTemp):
    while True:
        try:
            if exit == 0:
                time.sleep(3)
                temp = get_temp()
                if temp>lowTemp and temp<topTemp:
                    turn_off_both()
                    print("Ctrl+C to return to main menu")
                elif temp<lowTemp:
                    turn_on_heater()
                    print("Ctrl+C to return to main menu")
                elif temp>topTemp:
                    turn_on_fan()
                    print("Ctrl+C to return to main menu")
                else:
                    continue
            else:
                break
        except KeyboardInterrupt:
            break
        

def main():
    global opt
    global exit
    global topTemp
    global lowTemp
    opt = 0
    exit = 0
    topTemp = 24
    lowTemp = 18
    while True:
        try:
            menu = main_menu()
            if menu == 1:
                exit = normal_mode()
                polling_loop(exit,topTemp,lowTemp)
            elif menu == 2:
                menu = maintenance_mode()
            elif menu == 3:
                menu = data_obsv_mode()
            elif menu == 4:
                break
        except KeyboardInterrupt:
            print("Terminating program...")
    
if __name__ == "__main__":
    import time
    main()
