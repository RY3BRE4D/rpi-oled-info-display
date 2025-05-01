# Raspberry Pi OLED Info Display

This directory contains a project where Python is used to interface with an SSD1306 OLED display to show useful system information. The display presents:

- CPU usage and temperature
- RAM and disk usage
- Time since boot
- Current time and date
- IP Address
- And more features coming soon (like local weather)

The Python script is launched automatically at boot using `systemd`, and runs inside a dedicated virtual environment.

---


## Features

- SSD1306 OLED display support via the [Luma.OLED](https://github.com/rm-hull/luma.oled) library
- Auto-start on boot using a `systemd` service
- Lightweight and efficient display of live system stats
- Modular design for easy future feature additions

---


## Requirements

- Raspberry Pi OS (Lite or Full)
- Python 3
- Virtual environment (`venv`)
- Libraries:
  - `luma.oled`
  - `psutil`

---


## Hardware Setup

Hooking up the SSD1306 OLED is a breeze. Just four wires!

| SSD1306 Pin | Raspberry Pi Pin | Function        |
|-------------|------------------|-----------------|
| GND         | Pin 6            | Ground (GND)    |
| VCC         | Pin 1            | 3.3V or 5V Power|
| SCL         | Pin 5            | GPIO3 / I2C SCL |
| SDA         | Pin 3            | GPIO2 / I2C SDA |

---


## Installation

Follow these steps to install and run the project.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RY3BRE4D/rpi-oled-info-display.git
   cd rpi-oled-info-display
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the script:**
   ```bash
   python3 main.py
   ```
---


## Creating a Service That Runs The Script At Boot

Follow these steps to create a service that activates the venv
and starts the Python program at boot
1. **Edit info_oled.serivce to include the correct path:**
   open the service file with nano or any text editor:
   ```bash
   nano info_oled.service
   ```

   Specifically, edit these two lines in the file:
   ```ini
   ExecStart=/bin/bash -c 'source /home/pi/rpi-oled-info-display/venv/bin/activate && python /home/pi/rpi-oled-info-display/main.py'
   WorkingDirectory=/home/pi/rpi-oled-info-display
   ```

2. **Copy info_oled.service from project directory to systemd:**
   ```bash
   sudo cp info_oled.service /etc/systemd/system/
   ```

3. **Reload systemd to recognize the new service:**
   ```bash
   sudo systemctl daemon-reexec
   ```
4. **Enable the service to start at boot:**
   ```bash
   sudo systemctl enable info_oled.service
   ```
5. **Optionally start or check status of service:**
   ```bash
   sudo systemctl start info_oled.service
   sudo systemctl status info_oled.service
   ```
---


## License

This project is licensed under the [MIT License](LICENSE).

Note: This project depends on external libraries such as:
- [Luma.OLED](https://github.com/rm-hull/luma.oled)
- [Luma.Core](https://github.com/rm-hull/luma.core)
- [Pillow](https://python-pillow.org/)
- [psutil](https://github.com/giampaolo/psutil)
- [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/)

Each of these libraries is distributed under its own license. Refer to their individual repositories for license details.
