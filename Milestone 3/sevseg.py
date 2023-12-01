"""
Seven-Segment Display function file
Last edited by: Pandu Raditya Rohman
Version: 3
Last modified: 13/10/2023
"""

import time
serialPinSevseg = 7
rclckPinSevseg = 8
srclckPinSevseg = 9
onPins = [10,11,12,13]

def write_sevseg(msg,duration,board,onPins=onPins,serialPin=serialPinSevseg,rclckPin=rclckPinSevseg,srclckPin=srclckPinSevseg):
    """
    Function that shows a message on the seven segment display.


    Args:
        msg: Message on what wants to be written
        duration (Integer): How long you want the message to last
        board: The Arduino
        onPins (List): Pins to turn on/off the digits of the seven segment display
        serialPin (Integer): Digital pin number for the shift register's serial pin.
        rclckPin (Integer): Digital pin number for the shift register's register clock pin.
        srclckPin (Integer): Digital pin number for the shift register's serial clock pin..
    """
    lookupDictionary = {
    "0": "01111110",
    "1": "00110000",
    "2": "01101101",
    "3": "01111001",
    "4": "00110011",
    "5": "01011011",
    "6": "01011111",
    "7": "01110000",
    "8": "01111111",
    "9": "01111011",
    'A': '01110111',
    'B': '00011111',
    'C': '01001110',
    'D': '00111101',
    'E': '01001111',
    'F': '01001111',
    'G': '01011110',
    'H': '00010111',
    'I': '00000110',
    'J': '00111100',
    'K': '01010111',
    'L': '00001110',
    'M': '01010100',
    'N': '01110110',
    'O': '01111110',
    'P': '01100111',
    'Q': '01110011',
    'R': '01100110',
    'S': '01011011',
    'T': '00001111',
    'U': '00111110',
    'V': '00111010',
    'X': '00110111',
    'Y': '00111011',
    'Z': '01101001',
    ' ': '00000000',
    '*': '01100011'}
    
    for k in range(8):
        board.digital_pin_write(serialPin,0)
        board.digital_pin_write(srclckPin,1)
        time.sleep(0.0001)
        board.digital_pin_write(srclckPin,0)
    board.digital_pin_write(rclckPin,1)
    time.sleep(0.0001)
    board.digital_pin_write(rclckPin,0)
    
    msg = str(msg)
    values = []
    for m in range(len(msg)):
        values.append(msg[m])
    
    for k in range(len(msg)):
        try:
            values[k] = int(values[k])
        except ValueError:
            values[k] = values[k].upper()

    for j in range(len(values)):
        values[j] = lookupDictionary[str(values[j])]

    start = time.time()
    counter = 0
    while counter<=duration:
        
        if len(values)<=4:
            while len(values)!=4:
                values.append(lookupDictionary[' '])

            for i in range(len(values)):
                for j in range(len(values[i])):
                    board.digital_pin_write(serialPin,int(values[i][j]))
                    board.digital_pin_write(srclckPin,1)
                    time.sleep(0.0001)
                    board.digital_pin_write(srclckPin,0)
                board.digital_pin_write(rclckPin,1)
                board.digital_pin_write(onPins[i],0)
                time.sleep(0.0001)
                board.digital_pin_write(onPins[i],1)
                board.digital_pin_write(rclckPin,0)

        else:
            for l in range(len(msg)):
                temp = []
                for s in range(4):
                    if s+l<len(values):
                        temp.append(values[s+l])
                while len(temp)<4:
                    temp.append(lookupDictionary[' '])
                
                start2 = time.time()
                counter2 = 0
                while counter2<0.2:
                    for o in range(len(temp)):
                        for p in range(len(temp[o])):
                            board.digital_pin_write(serialPin,int(temp[o][p]))
                            board.digital_pin_write(srclckPin,1)
                            time.sleep(0.0001)
                            board.digital_pin_write(srclckPin,0)
                        board.digital_pin_write(rclckPin,1)
                        board.digital_pin_write(onPins[o],0)
                        time.sleep(0.0001)
                        board.digital_pin_write(onPins[o],1)
                        board.digital_pin_write(rclckPin,0)
                    counter2 = time.time()-start2
        
        counter = time.time() - start