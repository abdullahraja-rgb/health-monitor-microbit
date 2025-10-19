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


def update_graph(i):
    """
    This function is called by FuncAnimation to update the real-time plot.
    """
    if ser.in_waiting > 0:
        try:

            data = ser.readline().decode('utf-8').strip()
            print(f"Raw Data: {data}")  # Debugging


            parts = data.split()
            if len(parts) != 2:
                print("Unexpected data format (not 2 parts), skipping...")
                return

            temp_value = int(parts[0].split(':')[1])
            steps_value = int(parts[1].split(':')[1])
            timestamp_obj = datetime.now()
            

            csv_writer.writerow([timestamp_obj.strftime("%Y-%m-%d %H:%M:%S"), temp_value, steps_value])
            csv_file.flush()

 
            time_stamps.append(timestamp_obj.strftime("%H:%M:%S"))
            temperature_readings.append(temp_value)
            step_readings.append(steps_value)

            # Limit data points to last 50 for better visualization
            time_stamps[:] = time_stamps[-50:]
            temperature_readings[:] = temperature_readings[-50:]
            step_readings[:] = step_readings[-50:]


            ax1.clear()
            ax2.clear()
            
            ax1.plot(time_stamps, temperature_readings, 'r-', marker='o', label="Temperature")
            ax2.plot(time_stamps, step_readings, 'g-', marker='s', label="Steps")

            ax1.set_xlabel("Time")
            ax1.set_ylabel("Temperature (°C)", color='r')
            ax2.set_ylabel("Steps", color='g')
            ax1.tick_params(axis='y', colors='r')
            ax2.tick_params(axis='y', colors='g')
            ax1.tick_params(axis='x', rotation=45)
            
            fig.suptitle('Real-time Health Monitor', fontsize=16)
            fig.tight_layout(rect=[0, 0.03, 1, 0.95])
            
            # Add legends
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc='upper left')

            # Generate static graphs every 60 readings (approx 1 min)
            if len(time_stamps) % 60 == 0 and len(time_stamps) > 0:
                print("Generating static analysis graphs...")
                update_static_graphs()

        except (IndexError, ValueError, TypeError) as e:
            print(f"Error processing data '{data}': {e}. Skipping...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def update_static_graphs():
    """
    Reads the full CSV and generates a set of static analysis graphs.
    """
    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            print("CSV file is empty, skipping static graphs.")
            return

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Temperature (°C)'] = pd.to_numeric(df['Temperature (°C)'])
        df['Total Steps'] = pd.to_numeric(df['Total Steps'])


        df["Calories Burned"] = df["Total Steps"] * 0.04 # Simple approximation
        df['Time Diff'] = df['Timestamp'].diff().dt.total_seconds().fillna(0)
        df['Steps per Second'] = df['Total Steps'].diff().fillna(0) / df['Time Diff']
        df['Steps per Second'] = df['Steps per Second'].replace([float('inf'), -float('inf')], 0)


        # 1. Line Chart: Time vs Body Temperature
        plt.figure(figsize=(10, 5))
        plt.plot(df['Timestamp'], df['Temperature (°C)'], marker='o', color='r', label='Body Temp')
        plt.title('Body Temperature Over Time')
        plt.xlabel('Time')
        plt.ylabel('Body Temperature (°C)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('static_temp_over_time.png')
        plt.close()

        # 2. Line Chart: Time vs Total Steps
        plt.figure(figsize=(10, 5))
        plt.plot(df['Timestamp'], df['Total Steps'], marker='s', color='g', label='Total Steps')
        plt.title('Steps Over Time')
        plt.xlabel('Time')
        plt.ylabel('Total Steps')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('static_steps_over_time.png')
        plt.close()

        # 3. Scatter Plot: Total Steps vs Body Temperature
        plt.figure(figsize=(10, 5))
        sns.scatterplot(x=df['Total Steps'], y=df['Temperature (°C)'], color='b')
        plt.title('Body Temperature vs. Total Steps')
        plt.xlabel('Total Steps')
        plt.ylabel('Body Temperature (°C)')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('static_temp_vs_steps.png')
        plt.close()


        plt.figure(figsize=(10, 5))
        df_sampled = df.iloc[::5, :]
        plt.bar(df_sampled["Timestamp"], df_sampled["Calories Burned"], color='orange', width=0.5, label='Calories Burned')
        plt.title('Calories Burned Over Time')
        plt.xlabel('Time')
        plt.ylabel('Calories Burned')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('static_calories_over_time.png')
        plt.close()

        
        print("Static graphs saved as PNG files.")

    except pd.errors.EmptyDataError:
        print("CSV file is empty. No static graphs generated.")
    except Exception as e:
        print(f"Error generating static graphs: {e}")

try:
    print("Starting real-time visualization... Press Ctrl+C to stop.")
    # Animate the real-time plot, updating every 1000ms (1 second)
    ani = animation.FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)
    plt.show()

except KeyboardInterrupt:
    print("Stopping data logging...")

finally:
    # Cleanup on exit
    csv_file.close()
    ser.close()
    print("Serial port and CSV file closed. Exiting.")