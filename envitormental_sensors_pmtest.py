import adafruit_tsl2591

# environmental_sensors.py

import time
import datetime
import serial
import pynmea2
import board
import busio
import adafruit_ltr390
import adafruit_sgp40
from adafruit_bme280 import basic as adafruit_bme280
import struct
# -------------------------
# Initialize I2C and Sensors
# -------------------------

i2c = busio.I2C(board.SCL, board.SDA)

# UV Sensor
ltr = adafruit_ltr390.LTR390(i2c)

# Ambient Light Sensor
tsl = adafruit_tsl2591.TSL2591(i2c)

# VOC Sensor (initialized for global use after equilibration)
sgp = adafruit_sgp40.SGP40(i2c)


# Initialize sensors
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# -------------------------
# GPS: get_location
# -------------------------

#def get_location(port="/dev/ttyACM0", baudrate=9600, timeout=1):
#    """Returns (timestamp, latitude, longitude) from GPS module."""
#    ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
#    try:
#        while True:
#            line = ser.readline().decode('ascii', errors='replace')
#            if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
#                try:
#                    msg = pynmea2.parse(line)
#                    return msg.timestamp, msg.latitude, msg.longitude
#                except pynmea2.ParseError:
#                    continue
#    finally:
#        ser.close()
        
def get_location(port="/dev/ttyACM0", baudrate=9600, timeout=1):
    """Returns (timestamp, latitude, longitude) with full timestamp from GPS."""
    ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
    try:
        while True:
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith('$GPRMC'):
                try:
                    msg = pynmea2.parse(line)
                    if msg.status == 'A':  # Valid fix
                        # Combine date and time into full timestamp
                        date = msg.datestamp  # datetime.date
                        time = msg.timestamp  # datetime.time
                        full_dt = datetime.datetime.combine(date, time).isoformat()
                        return full_dt, msg.latitude, msg.longitude
                except pynmea2.ParseError:
                    continue
            elif line.startswith('$GPGGA'):
                # Optional fallback if GPRMC fails
                continue
    finally:
        ser.close()

# -------------------------
# UV Sensor: get_uv
# -------------------------

def get_uv():
    """Returns (uv_raw, uv_index) from LTR390 UV sensor."""
    uv_raw = ltr.uvs
    uv_index = ltr.uvi
    return uv_raw, uv_index

# -------------------------
# VOC Sensor Functions
# -------------------------

def equilibrate_voc(duration=120):
    """Equilibrate VOC sensor for the specified duration in seconds."""
    print(f"Equilibrating VOC sensor for {duration} seconds...")
    for i in range(duration):
        sgp.measure_raw()
        time.sleep(1)
    print("VOC sensor equilibration complete.")

# -------------------------
# VOC Sensor (with compensation from BME280)
# -------------------------

def get_voc():
    """Returns compensated VOC index, temperature, and humidity."""
    temperature = bme280.temperature
    humidity = bme280.humidity
    voc_index = sgp.measure_index(
        temperature=temperature,
        relative_humidity=humidity
    )
    return voc_index, temperature, humidity

# -------------------------
# Get Visible, Lux, IR data
# -------------------------

def get_lux():
    """Return ambient light in lux."""
    return tsl.lux


def get_visible():
    """Return raw visible light value."""
    return tsl.visible


def get_ir():
    """Return raw infrared light value."""
    return tsl.infrared

# -------------------------
# Get PM Data
# -------------------------
def get_pm():
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
    return read_pm_data()


# -------------------------
# Combined Sensor Data Collection
# -------------------------

def get_all_sensor_data():
    """
    vis = get_visible()
    ir = get_ir()
    lux = get_lux()
    Returns a dictionary containing:
    - GPS: timestamp, latitude, longitude
    - UV sensor: uv_raw, uv_index
    - VOC sensor: voc_index, temperature (°C), humidity (%RH)
    Assumes VOC sensor has been equilibrated.
    """
    timestamp, lat, lon = get_location()
    voc_index, temp, humidity = get_voc()
    vis = get_visible()
    ir = get_ir()
    lux = get_lux()
    uv_raw, uv_index = get_uv()
    pm1_0, pm2_5, pm10 = get_pm()

    return {
        "timestamp": timestamp,
        "latitude": lat,
        "longitude": lon,
        "voc_index": voc_index,
        "temperature_C": temp,
        "humidity_percent": humidity,
        "uv_raw": uv_raw,
        "uv_index": uv_index,
        "visible": vis,
        "infrared": ir,
        "lux": lux,
        "pm1_0": pm1_0,
        "pm2_5": pm2_5,
        "pm10": pm10

    }
