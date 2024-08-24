from serial import Serial
from constants import SHOULD_USE_ARDUINO_FLASH

# [0, 255]
def flash(duration_ms):
    if SHOULD_USE_ARDUINO_FLASH:
        arduino = Serial(port='COM5', baudrate=2400, timeout=.1)
        arduino.write((duration_ms).to_bytes())

if __name__ == '__main__':
    arduino = Serial(port='COM5', baudrate=2400, timeout=.1)
    while True:
        n = int(input("Enter a number: "))
        flash(n)