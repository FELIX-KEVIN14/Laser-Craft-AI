# laser_control.py

import serial
import time
import logging
import os
import sys

def setup_logger():
    logger = logging.getLogger('LaserControl')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('laser_control.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

class LaserController:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        logger.info(f"Connecting to laser cutter on port {self.port} at {self.baudrate} baud.")
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Wait for connection to establish
            logger.info("Connection established.")
        except serial.SerialException as e:
            logger.error(f"Failed to connect to laser cutter: {e}")
            raise

    def disconnect(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("Disconnected from laser cutter.")

    def send_command(self, command):
        if self.connection and self.connection.is_open:
            logger.debug(f"Sending command: {command}")
            self.connection.write((command + '\n').encode())
            response = self.connection.readline().decode().strip()
            logger.debug(f"Received response: {response}")
            return response
        else:
            logger.error("Attempted to send command without an active connection.")
            raise ConnectionError("Not connected to laser cutter.")

    def send_gcode_file(self, filepath):
        if not os.path.exists(filepath):
            logger.error(f"G-code file {filepath} does not exist.")
            raise FileNotFoundError(f"G-code file {filepath} not found.")
        logger.info(f"Sending G-code file: {filepath}")
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    self.send_command(line)
                    time.sleep(0.1)  # Delay between commands
        logger.info("G-code file transmission completed.")

    def start_laser(self):
        logger.info("Starting laser.")
        self.send_command('M3')  # Example command to start laser

    def stop_laser(self):
        logger.info("Stopping laser.")
        self.send_command('M5')  # Example command to stop laser

    def move_to(self, x, y, feed_rate=1000):
        command = f"G1 X{x} Y{y} F{feed_rate}"
        logger.info(f"Moving to position: X={x}, Y={y}, Feed Rate={feed_rate}")
        self.send_command(command)

    def home(self):
        logger.info("Homing all axes.")
        self.send_command('G28')  # Home all axes

def main():
    controller = LaserController()
    try:
        controller.connect()
        controller.home()
        controller.start_laser()
        controller.move_to(10, 10)
        controller.move_to(20, 20)
        controller.stop_laser()
        controller.disconnect()
    except Exception as e:
        logger.exception("An error occurred in the laser control module.")
        controller.disconnect()
        sys.exit(1)

if __name__ == '__main__':
    main()
