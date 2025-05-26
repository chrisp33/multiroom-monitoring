import time
import board
import busio

# Import LTR390 for UV
import adafruit_ltr390

# Import TSL2591 for ambient light
import adafruit_tsl2591

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensors
ltr = adafruit_ltr390.LTR390(i2c)
tsl = adafruit_tsl2591.TSL2591(i2c)

# Reduce gain to prevent overflow in bright light
tsl.gain = adafruit_tsl2591.GAIN_LOW  # Options: LOW, MED, HIGH, MAX

print("LTR390 (UV) + TSL2591 (ALS) Sensor Test")
print("----------------------------------------")

while True:
    try:
        # LTR390 values
        ambient_raw = ltr.light     # Raw visible light (ALS)
        uv_raw = ltr.uvs            # Raw UV signal
        uv_index = ltr.uvi          # UV Index

        # TSL2591 values
        lux = tsl.lux               # Human-perceived brightness in lux
        visible = tsl.visible       # Raw visible
        ir = tsl.infrared           # Raw infrared
        full = tsl.full_spectrum    # Raw visible + IR

        # Print values
        print(f"UV Raw: {uv_raw} | UV Index: {uv_index:.2f}")
        print(f"LTR390 Visible Raw: {ambient_raw}")
        #print(f"TSL2591 Lux: {lux:.2f} | Visible: {visible} | IR: {ir} | Full: {full}")
        print("-" * 50)
        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)
