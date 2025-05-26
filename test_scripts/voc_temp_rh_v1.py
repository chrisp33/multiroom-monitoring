import time
import board
import busio
import adafruit_sgp40
from adafruit_bme280 import basic as adafruit_bme280

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensors
sgp = adafruit_sgp40.SGP40(i2c)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

print("Starting VOC + Temp + Humidity Monitoring...\n")

# Optional warm-up
print("Warming up the SGP40 sensor for 10 seconds...")
for i in range(10):
    print(".", end="", flush=True)
    time.sleep(1)

print("\nMonitoring started.\n")

# Continuous readings
while True:
    try:
        temperature = bme280.temperature      # °C
        humidity = bme280.humidity            # % RH

        voc_index = sgp.measure_index(
            temperature=temperature,
            relative_humidity=humidity
        )

        print(f"Temp: {temperature:.1f} °C | RH: {humidity:.1f} % | VOC Index: {voc_index}")
        time.sleep(5)

    except KeyboardInterrupt:
        print("\nExiting...")
        break
