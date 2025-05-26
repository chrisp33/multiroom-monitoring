import serial
import struct

def sync_to_frame(ser):
    while True:
        b1 = ser.read(1)
        if b1 == b'\x42':
            b2 = ser.read(1)
            if b2 == b'\x4d':
                return b'\x42' + b'\x4d' + ser.read(30)

def read_pm_data():
    ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=2)
    try:
        data = sync_to_frame(ser)
        frame = struct.unpack(">HHHHHHHHHHHHHH", data[4:])
        pm1_0 = frame[0]
        pm2_5 = frame[1]
        pm10 = frame[2]
        return pm1_0, pm2_5, pm10
    except Exception as e:
        print("Error reading PM sensor:", e)
        return None, None, None
    finally:
        ser.close()
