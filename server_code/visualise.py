import serial
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation
from datetime import datetime
import os


SERIAL_PORT = "COM5" 
BAUD_RATE = 115200
CSV_FILE = 'sensor_data.csv'


# Configure the serial connection to the Microbit
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} bps.")
except serial.SerialException as e:
    print(f"Error: Could not open port {SERIAL_PORT}. {e}")
    print("Please check the port name and ensure the micro:bit is connected.")
    exit()

# Prepare CSV file
file_exists = os.path.isfile(CSV_FILE)
csv_file = open(CSV_FILE, 'a', newline='')
csv_writer = csv.writer(csv_file)
if not file_exists:
    csv_writer.writerow(['Timestamp', 'Temperature (°C)', 'Total Steps'])
    csv_file.flush()
    print("Created new CSV file with headers.")

# Lists for real-time graphing
time_stamps = []
temperature_readings = []
step_readings = []

# Setup Matplotlib figure for real-time graph
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()