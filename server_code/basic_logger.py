import serial
import csv
from datetime import datetime
import os


SERIAL_PORT = "COM5"  # <<< UPDATE THIS to your micro:bit's port
BAUD_RATE = 115200
CSV_FILE = 'sensor_data_basic.csv'

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} bps.")
except serial.SerialException as e:
    print(f"Error: Could not open port {SERIAL_PORT}. {e}")
    print("Please check the port name and ensure the micro:bit is connected.")
    exit()

# Open or create a CSV file for logging
file_exists = os.path.isfile(CSV_FILE)
csv_file = open(CSV_FILE, 'a', newline='')
csv_writer = csv.writer(csv_file)

# Write header if file is new
if not file_exists:
    csv_writer.writerow(['Timestamp', 'Temperature (°C)', 'Steps'])
    csv_file.flush()
    print(f"Created new file: {CSV_FILE}")

print("Listening for data from MicroBit server... Press Ctrl+C to stop.")

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if not data:
                continue
            
            print(f"Raw Data: {data}")  # Debugging line
            
            try:
                # Split incoming data assuming format "Temp:25 Steps:1000"
                parts = data.split()
                if len(parts) != 2:
                    print("Unexpected data format (not 2 parts), skipping...")
                    continue
                
                temp_value = int(parts[0].split(':')[1])  # Extract temperature
                steps_value = int(parts[1].split(':')[1])  # Extract steps
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Write to CSV
                csv_writer.writerow([timestamp, temp_value, steps_value])
                csv_file.flush()  # Ensure data is written immediately
                
                print(f"Logged: {timestamp}, Temp: {temp_value}°C, Steps: {steps_value}")
                
            except (IndexError, ValueError) as e:
                print(f"Error processing data '{data}': {e}. Skipping...")

except KeyboardInterrupt:
    print("\nData logging stopped by user.")

finally:
    csv_file.close()
    ser.close()
    print("CSV file and serial port closed.")