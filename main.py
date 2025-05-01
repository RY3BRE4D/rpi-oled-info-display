"""
Package Name: Raspberry Pi OLED Info Display
Description: Shows Useful Information On An OLED Display
Author: Ryan Frost
Version: 1.0.0
License: MIT
Last Modified: 2025-04-27
"""


import atexit
import signal
import sys
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import psutil
import os
import RPi.GPIO as pins
pins.setmode(pins.BCM)  #Set To BOARD Pin Number Configuration (Or Use BCM)
from time import sleep
import datetime
import socket


# Function To Clear the OLED Display
def clearDisplay():
    draw.rectangle((0, 0, dispWidth, dispHeight), outline=0, fill=0)
    myDisplay.display(image)

# Function To Clear Draw A Black Rectangle On The OLED Display But Not Display It
def quickClearDisplay():
    draw.rectangle((0, 0, dispWidth, dispHeight), outline=0, fill=0)

# Function To Clear The Terminal
def clearTerminal():
    if os.name == 'nt':    # For Windows
        os.system('cls')
    else:                   # For Linux
        os.system('clear')

# Functions To Exit The Program Gracefully
def cleanup():
    print('Cleaning Up!')
    pins.cleanup()
    #clearDisplay()
atexit.register(cleanup)                           # Register The Cleanup Function
def signalHandler(signum, frame):
    print(f"Received signal {signum}, exiting...")
    sys.exit(0)
# Register The Signal Handler
signal.signal(signal.SIGTERM, signalHandler)  # Sent by `kill` or system shutdown
signal.signal(signal.SIGHUP, signalHandler)   # Sent by terminal hang-up (or session end)
#signal.signal(signal.SIGINT, signalHandler)   # Sent by Ctrl+C


# Getting The IP Address Of The Device
def getIPAddress():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        return ip
    except Exception as e:
        return None


# Initialize The Display
interface = i2c(port=1, address=0x3C)
myDisplay = ssd1306(interface, width=128, height=64)
dispHeight = myDisplay.height
dispWidth = myDisplay.width
image = Image.new('1', (dispWidth, dispHeight))
draw = ImageDraw.Draw(image)
#font = ImageFont.load_default()
font = ImageFont.truetype('font1.ttf', 18)
headerFont = ImageFont.truetype('font1.ttf', 12)
clearDisplay()

# Setting Up The Button That Will Switch The State Of The OLED Display
sButton = 18
buttonStateOld = 1    # Variable For Storing The Button State From The Last Loop
buttonState = 1       # Variable For Storing The Current Button State
pins.setup(sButton,pins.IN,pull_up_down=pins.PUD_UP) # Setting Up The Button As An Input Pullup Resistor Active
oledState = 0        # Variable For Storing The State Of The OLED Display



# Function To Display The CPU Usage And Temp
def oledState0():
    # Get The CPU Temp
    temperatures = psutil.sensors_temperatures()
    if temperatures:
        cpuTemp =  round(float(temperatures['cpu_thermal'][0].current),0)
    else:
        print("No Temps Available!")

    # Get CPU Usage
    cpuUsage = psutil.cpu_percent(interval=.1)

    # Get Memory Usage
    memory = psutil.virtual_memory()
    memoryUsage = memory.percent
    memoryLeft = f'{memory.available / (1024**3):.2f}GB'

    # Clear The Terminal And Print The CPU Usage And Temp
    clearTerminal()
    print(f"CPU Usage: {cpuUsage}%")
    print(f"CPU Temp: {cpuTemp}°C")
    print(f"Memory Usage: {memoryUsage}%")
    print(f"Memory Left: {memoryLeft}")

    quickClearDisplay()
    header = "CURRENT METRICS"
    # Draws Text
    draw.text(((dispWidth/2)-(len(header)*8/2), 0), header, font=headerFont, fill=255)
    draw.text((0, 15), "  CPU:", font=headerFont, fill=255)
    draw.text((75, 15), "  RAM:", font=headerFont, fill=255)
    draw.text((0, 28), f"{cpuUsage}%", font=font, fill=255)
    draw.text((0, 45), f"{cpuTemp}°C", font=font, fill=255)
    draw.text((68, 28), f"{memoryUsage}%", font=font, fill=255)
    draw.text((68, 45), f"{memoryLeft}", font=font, fill=255)
    myDisplay.display(image)


# Function To Display The Time Since Boot
def oledState1():
    # Get Elapsed Time Since Boot
    with open('/proc/uptime', 'r') as f:
        elapsedT = float(f.readline().split()[0])
    eTMin = elapsedT / 60
    eTHour = eTMin / 60
    eTDay = eTHour / 24
    eDays = int(eTDay)
    eHours = int(eTHour%24)
    eMins = int(eTMin%60)
    eSecs = int(elapsedT%60)

    # Clear The Terminal And Print The Boot Time And Elapsed Time
    clearTerminal()
    print(f"Elapsed Time: {eDays} Days, {eHours} Hours, {eMins} Minutes, {eSecs} Seconds")

    quickClearDisplay()
    header = "TIME SINCE BOOT"
    # Draws Text
    draw.text(((dispWidth/2)-(len(header)*7/2), 0), header, font=headerFont, fill=255)
    draw.text((0, 15), f"{eDays} DAYS", font=headerFont, fill=255)
    draw.text((0, 28), f"{eHours} HOURS", font=headerFont, fill=255)
    draw.text((0, 41), f"{eMins} MINUTES", font=headerFont, fill=255)
    draw.text((0, 54), f"{eSecs} SECONDS", font=headerFont, fill=255)
    myDisplay.display(image)


# Function To Display The Current Time
def oledState2():
    # Get The Current Time
    currentDate = datetime.datetime.now().strftime("%m-%d-%Y")
    currentTime = datetime.datetime.now().strftime("%I:%M:%S %p")

    # Clear The Terminal And Print The Current Time
    clearTerminal()
    print(f"Current Date: {currentDate}")
    print(f"Current Time: {currentTime}")

    quickClearDisplay()
    header = "CURRENT TIME"
    # Draws Text
    draw.text(((dispWidth/2)-(len(header)*8/2), 0), header, font=headerFont, fill=255)
    draw.text(((dispWidth/2)-(len(currentDate)*10/2), 15) , f"{currentDate}", font=font, fill=255)
    draw.text(((dispWidth/2)-(len(currentTime)*10/2), 40), f"{currentTime}", font=font, fill=255)
    myDisplay.display(image)



# Function To Display The IP Address
def oledState3():
    # Get The IP Address
    ip = getIPAddress()
    if ip:
        print(f"IP Address: {ip}")
    else:
        print("No IP Address Available!")

    # Clear The Terminal And Print The IP Address
    clearTerminal()
    print(f"IP Address: {ip}")

    quickClearDisplay()
    header = "IP ADDRESS"
    # Draws Text
    draw.text(((dispWidth/2)-(len(header)*8/2), 0), header, font=headerFont, fill=255)
    draw.text(((dispWidth/2)-(len(ip)*10/2), 15), f"{ip}", font=font, fill=255)
    myDisplay.display(image)


def main():
    global oledState, buttonStateOld, buttonState
    try:
        while True:
            buttonState = pins.input(sButton)
            #print(buttonState)
            if buttonStateOld ==0 and buttonState == 1:
                if oledState == 0:
                    oledState = 1
                elif oledState == 1:
                    oledState = 2
                elif oledState == 2:
                    oledState = 3
                elif oledState == 3:
                    oledState = 0
                else:
                    print('Error!')

            buttonStateOld = buttonState

            if oledState == 0:
                oledState0()
            elif oledState == 1:
                oledState1()
            elif oledState == 2:
                oledState2()
            elif oledState == 3:
                oledState3()
            sleep(.1)


    except KeyboardInterrupt:
            pass
    except Exception as e:
            print(f"An error occurred: {e}")
            cleanup()
    finally:
            clearTerminal()
            print('Exiting...')


if __name__ == "__main__":
    main()



    
