import serial
arduino = serial.Serial(port='COM5', baudrate=2400, timeout=.1)

# [0, 255]
def flash(duration_ms):
    arduino.write((duration_ms).to_bytes())

if __name__ == '__main__':
    while True:
        n = int(input("Enter a number: "))
        flash(n)