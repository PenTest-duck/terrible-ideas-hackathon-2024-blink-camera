# import time
import serial
from constants import SHOULD_USE_ARDUINO
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)

arduino.write(bytes("\n", 'ascii'))  # first byte is ignored for some reason

def flash():
    if SHOULD_USE_ARDUINO:
        arduino.write(bytes("F\n", 'ascii'))

def off():
    if SHOULD_USE_ARDUINO:
        arduino.write(bytes("O\n", 'ascii'))

def clear():
    if SHOULD_USE_ARDUINO:
        arduino.write(bytes("C\n", 'ascii'))

def slide_on():
    if SHOULD_USE_ARDUINO:
        arduino.write(bytes("S\n", 'ascii'))

def set_region(start, end, colour):
    if SHOULD_USE_ARDUINO:
        arduino.write(bytes(f"R {start} {end} {colour}\n", 'ascii'))

if __name__ == '__main__':
    while True:
    #    n = int(input("Enter a number: "))
    #    flash(n)
        string = input("Enter a string: ") + "\n"
        print(string)
        b = bytes(string, 'ascii')
        print(b)
        arduino.write(b)

        #time.sleep(5)
        #data = arduino.read_all().decode('utf-8') 
        #print(f"response: {data}")

