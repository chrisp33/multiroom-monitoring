import csv
import os
from all_sensors import *

def log_sensor_data_to_csv(filename="data.csv"):
    """
    Collects full sensor data and appends it to a CSV file.
    Creates the file and writes headers if it does not exist.
    """
    data = get_all_sensor_data()
    fieldnames = [
        "timestamp", "latitude", "longitude",
        "voc_index", "temperature_C", "humidity_percent",
        "visible", "infrared", "lux", "uv_raw", "uv_index",
        "pm1_0", "pm2_5", "pm10"
    ]

    file_exists = os.path.isfile(filename)

    try:
        with open(filename, mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write headers only once
            if not file_exists:
                writer.writeheader()

            writer.writerow(data)

        print(f"Logged data to {filename}")

    except Exception as e:
        print(f"[ERROR] Failed to write to CSV: {e}")
        
if __name__ == "__main__":
    try:
        equilibrate_voc(5)  # Warm up the VOC sensor before logging

        while True:
            log_sensor_data_to_csv("data.csv")
            time.sleep(60)  # Wait 60 seconds between measurements

    except KeyboardInterrupt:
        print("\nLogging stopped by user.")
