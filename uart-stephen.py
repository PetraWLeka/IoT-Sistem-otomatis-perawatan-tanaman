import serial
import tkinter as tk
import sqlite3

conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
             (soil_moisture INTEGER, light_sensor INTEGER, led_status INTEGER, water_pump_status INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()


ser = serial.Serial('/dev/ttyACM1', 9600)  # Set the serial port and baud rate

# Function to read the data from Arduino
def readData():
    data = ser.readline().decode('utf-8')
    if data:
        data_list = data.strip().split(',')
        try:
            data_list = [float(i) for i in data_list]
        except ValueError:
            print("VALUE EROR")
            window.after(1000, readData)
            return
        if (len(data_list) < 3):
            print()
        else:
            print(data_list)
            soil_moisture = data_list[0]
            light_sensor = data_list[1]
            led_status = data_list[2]
            water_pump_status = data_list[3]
            soil_moisture_label.config(
                text="Soil Moisture: {}".format(soil_moisture))
            light_sensor_label.config(text="Light Sensor: {}".format(light_sensor))
            led_status_label.config(text="LED Status: {}".format(led_status))
            water_pump_status_label.config(
                text="Water Pump Status: {}".format(water_pump_status))
            
            c.execute("INSERT INTO sensor_data (soil_moisture, light_sensor, led_status, water_pump_status) VALUES (?, ?, ?, ?)", (soil_moisture, light_sensor, led_status, water_pump_status))
            conn.commit()


    # Schedule the function to be called again in 1 second
    window.after(1000, readData)



# Function to turn on the LED


def turnOnLED():
    # Send the command to turn on the LED
    ser.write(b'1')
    led_status_label.config(text="LED Status: ON")

# Function to turn off the LED


def turnOffLED():
    # Send the command to turn off the LED
    ser.write(b'0')
    led_status_label.config(text="LED Status: OFF")

# Function to turn on the water pump


def turnOnWaterPump():
    # Send the command to turn on the water pump
    ser.write(b'2')
    water_pump_status_label.config(text="Water Pump Status: ON")

# Function to turn off the water pump


def turnOffWaterPump():
    # Send the command to turn off the water pump
    ser.write(b'3')
    water_pump_status_label.config(text="Water Pump Status: OFF")


# Create the tkinter window and add the labels and buttons
window = tk.Tk()
window.title("Arduino Data")
window.geometry("400x300")

soil_moisture_label = tk.Label(window, text="Soil Moisture: ")
soil_moisture_label.pack()

light_sensor_label = tk.Label(window, text="Light Sensor: ")
light_sensor_label.pack()

led_status_label = tk.Label(window, text="LED Status: ")
led_status_label.pack()

water_pump_status_label = tk.Label(window, text="Water Pump Status: ")
water_pump_status_label.pack()

led_on_button = tk.Button(window, text="Turn LED On", command=turnOnLED)
led_on_button.pack()

led_off_button = tk.Button(window, text="Turn LED Off", command=turnOffLED)
led_off_button.pack()

water_pump_on_button = tk.Button(
    window, text="Turn Water Pump On", command=turnOnWaterPump)
water_pump_on_button.pack()

water_pump_off_button = tk.Button(
    window, text="Turn Water Pump Off", command=turnOffWaterPump)
water_pump_off_button.pack()

# Read the data from Arduino every 1 second
window.after(1000, readData)

window.mainloop()
