"""
Seven-Segment Display function file
Created by: Pandu Raditya Rohman
Version: 2 
Last modified: 12/09/2023
"""
import time
segPins = [3,4,5,6,7,8,9]
onPins = [10,11,12,13]
def write_sevseg(msg,board,onPins=onPins,segPins=segPins):
    """
    Function that shows a message on the seven segment display.
    
    Parameters:
        msg: Message on what 
        board: The Arduino
        onPins: Pins to turn on/off the digits of the seven segment display
        segPins: Segment pins (a,b,c...) for the seven segment display
        
    Return:
        None
    """
    lookupDictionary = {
    "0": "1111110",
    "1": "0110000",
    "2": "1101101",
    "3": "1111001",
    "4": "0110011",
    "5": "1011011",
    "6": "1011111",
    "7": "1110000",
    "8": "1111111",
    "9": "1111011",
    'A': '1110111',
    'B': '0011111',
    'C': '1001110',
    'D': '0111101',
    'E': '1001111',
    'F': '1001111',
    'G': '1011110',
    'H': '0010111',
    'I': '0000110',
    'J': '0111100',
    'K': '1010111',
    'L': '0001110',
    'M': '1010100',
    'N': '1110110',
    'O': '1111110',
    'P': '1100111',
    'Q': '1110011',
    'R': '1100110',
    'S': '1011011',
    'T': '0001111',
    'U': '0111110',
    'V': '0111010',
    'X': '0110111',
    'Y': '0111011',
    'Z': '1101001',
    ' ': '0000000',
    '*': '1100011'}
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

    if len(values)<=4:
        while len(values)!=4:
            values.append(lookupDictionary[' '])

        for i in range(len(values)):
            for j in range(len(values[i])):
                board.digital_pin_write(segPins[j],int(values[i][j]))
            board.digital_pin_write(onPins[i],0)
            time.sleep(0.0001)
            board.digital_pin_write(onPins[i],1)
    else:
        for l in range(len(msg)):
            temp = []
            for s in range(4):
                if s+l<len(values):
                    temp.append(values[s+l])
            while len(temp)<4:
                temp.append(lookupDictionary[' '])
                
            for o in range(len(temp)):
                for p in range(len(temp[o])):
                    board.digital_pin_write(segPins[p],int(temp[o][p]))
                board.digital_pin_write(onPins[o],0)
                board.digital_pin_write(onPins[o],1)
            time.sleep(0.05)