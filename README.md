Here’s an updated version of your README based on your multi-sensor Raspberry Pi setup:

⸻

🏡 Multiroom Environmental Monitoring

This project collects environmental data from multiple sensors connected to a Raspberry Pi. Data is logged continuously and stored in CSV format for easy analysis.

🔧 Current Sensors Integrated
	•	VOC Sensor (SGP40)
	•	Temperature & Humidity Sensor (BME280)
	•	UV Sensor (LTR390)
	•	Ambient Light Sensor (TSL2591)
	•	Particulate Matter Sensor (PMS5003 via UART)
	•	GPS Module (USB Serial, NMEA via pynmea2)

📦 Data Collected

Each record includes:

| Field                    | Description                                   |
|--------------------------|-----------------------------------------------|
| timestamp                | ISO timestamp from GPS                        |
| latitude                 | From GPS module                               |
| longitude                | From GPS module                               |
| voc_index                | Compensated VOC index from SGP40               |
| temperature_C            | Temperature from BME280                        |
| humidity_percent         | Humidity from BME280                           |
| uv_raw, uv_index         | Raw UV value and UV index from LTR390          |
| visible, infrared, lux   | Ambient light channels from TSL2591            |
| pm1_0, pm2_5, pm10       | PM readings from PMS5003                       |

📁 File Structure
	•	environmental_sensors.py: Sensor initialization and readout functions
	•	run_experiment.py: Script for VOC equilibration and data logging loop
	•	test_scripts/: Folder with one-off test scripts for debugging individual components
	•	environment.yml: Conda environment specification

▶️ Running the Experiment

python run_experiment.py

	•	Logs data to data.csv by default.
	•	Equilibrates VOC sensor for 10–120 seconds before logging.
	•	CSV headers are written once; all subsequent rows are appended.

💾 Sample Output

| timestamp                  | latitude    | longitude         | voc_index | temperature_C | humidity_percent | visible | infrared | lux | uv_raw | uv_index | pm1_0 | pm2_5 | pm10 |
|----------------------------|-------------|-------------------|-----------|---------------|------------------|---------|----------|-----|--------|----------|-------|-------|------|
| 2025-05-27T20:09:21+00:00   | 39.0959455  | -198.23472566666667 | 0.24      | 22.1          | 43.0             | 45      | 251      | 102 | 10     | 20       | 0     | 0     | 0    |

🧪 Notes
	•	Ensure all sensors are wired properly before running.
	•	GPS is optional—errors are handled gracefully if not connected.
	•	PMS5003 uses /dev/serial0 by default.
	•	VOC may take an hour to equilibrate and stabilize. 
	•   Currently running Pi 4B with the latest Debian Bookworm
	•	Ensure serial ports are active on Pi. 

⸻