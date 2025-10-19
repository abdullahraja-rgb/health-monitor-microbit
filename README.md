# Micro:bit Health Monitor

This project is a simple health monitoring system built with BBC micro:bits. It uses a small wireless network to collect temperature and step-count data, which is then sent to a PC for logging and real-time visualization.

This project was developed for a university group project.

-----

## Features

  * **Wireless Data Collection:** Uses the micro:bit `radio` module to create a simple sensor network.
  * **Step Counting:** One micro:bit acts as a pedometer using the built-in accelerometer.
  * **Temperature Sensing:** A second micro:bit reads the ambient temperature from its internal sensor.
  * **Central Data Bridge:** A third micro:bit polls the sensors and forwards their data to a PC via USB serial.
  * **PC Data Logging:** A Python script on the PC logs all incoming data to a `sensor_data.csv` file.
  * **Data Visualisation:** The PC script uses `matplotlib` and `seaborn` to generate real-time graphs and periodic static analysis charts.

-----

## Project Structure

```
health-monitor-microbit/
├── microbit_code/
│   ├── server_bridge.py    # Code for the micro:bit connected to the PC
│   ├── sensor_steps.py     # Code for the step-counting sensor
│   └── sensor_temp.py      # Code for the temperature sensor
├── pc_app/
│   ├── visualise.py        # Main PC app for logging and graphing
│   ├── basic_logger.py     # A simpler script for only logging to CSV
│   └── requirements.txt    # Python libraries needed for the PC app
├── .gitignore
└── README.md
```

-----

## Hardware Requirements

  * **3 x BBC micro:bit**
  * **1 x PC** (Windows, Mac, or Linux)
  * **1 x Micro USB Cable** (to connect the server micro:bit)
  * **2 x Battery Packs** (for the two mobile sensors)

-----

## How to Use

### 1\. Program the Micro:bits

You will need to flash the code onto each micro:bit, for example, using the [Micro:bit Python Editor](https://python.microbit.org/v/3).

1.  **Step Sensor:** Flash the code from `microbit_code/sensor_steps.py` onto the first micro:bit. Attach a battery pack.
2.  **Temperature Sensor:** Flash the code from `microbit_code/sensor_temp.py` onto the second micro:bit. Attach a battery pack.
3.  **Server/Bridge:** Flash the code from `microbit_code/server_bridge.py` onto the third micro:bit. Connect this one directly to your PC with the USB cable.

### 2\. Set up the PC Application

1.  **Clone this repository:**

    ```bash
    git clone [your-repository-url]
    cd health-monitor-microbit/pc_app
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Find your COM Port:**
    You must find the port your micro:bit is connected to.

      * **Windows:** Open Device Manager. Look under "Ports (COM & LPT)" for "mbed Serial Port" or "USB Serial Device" (e.g., `COM5`).
      * **Mac:** Open Terminal and run `ls /dev/tty.*`. Look for `/dev/tty.usbmodem...`.
      * **Linux:** Open Terminal and run `ls /dev/tty*`. Look for `/dev/ttyACM0`.

5.  **Update the script:**
    Open the `pc_app/visualise.py` file in a text editor. On line 12, change `"COM5"` to the port you found in the previous step.

    ```python
    # Find this line (around line 12)
    ser = serial.Serial("COM5", 115200, timeout=1)  # <-- CHANGE "COM5"
    ```

6.  **Run the application:**
    Make sure your two sensor micro:bits are on and running. Then, run the script from your terminal:

    ```bash
    python visualise.py
    ```

The script will connect to the micro:bit, start logging data to `sensor_data.csv`, and open a window showing the live temperature and step-count graphs.
