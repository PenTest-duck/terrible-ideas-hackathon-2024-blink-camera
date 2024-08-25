# import time
import serial
from constants import SHOULD_USE_ARDUINO
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)

arduino.write((10).to_bytes())  # first byte is ignored for some reason

def flash(duration_ms):
    if SHOULD_USE_ARDUINO:
        arduino.write(duration_ms.to_bytes())

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

