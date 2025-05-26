import serial
import pynmea2
from time import sleep

port = "/dev/ttyACM0"
ser = serial.Serial(port, baudrate=9600, timeout=1)

print("Reading raw NMEA sentences...\n")

try:
    while True:
        line = ser.readline().decode('ascii', errors='replace')
        if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
            try:
                msg = pynmea2.parse(line)
                print(f"Time: {msg.timestamp}, Lat: {msg.latitude}, Lon: {msg.longitude}")
                sleep(5)
            except pynmea2.ParseError:
                continue
except KeyboardInterrupt:
    ser.close()
    print("\nStopped.")

