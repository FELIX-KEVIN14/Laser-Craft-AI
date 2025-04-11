import logging
import sys
import math

def setup_logger():
    logger = logging.getLogger('PathPlanner')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('path_planner.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

class PathPlanner:
    def __init__(self, material_class):
        self.material_class = material_class
        self.feed_rate = self.get_feed_rate()

    def get_feed_rate(self):
        logger.info(f"Determining feed rate for material class {self.material_class}.")
        feed_rates = {
            0: 1000,
            1: 800,
            2: 600
        }
        rate = feed_rates.get(self.material_class, 500)
        logger.info(f"Feed rate set to {rate}.")
        return rate

    def generate_circle_gcode(self, radius):
        logger.info(f"Generating G-code for circle with radius {radius}.")
        gcode = [
            f"G21 ; Set units to millimeters",
            f"G90 ; Absolute positioning",
            f"G1 F{self.feed_rate} ; Set feed rate",
            f"G0 X0 Y0 ; Move to origin",
            f"G2 X0 Y0 I{radius} J0 ; Clockwise circle"
        ]
        return '\n'.join(gcode)

    def generate_square_gcode(self, size):
        logger.info(f"Generating G-code for square with size {size}.")
        half_size = size / 2
        gcode = [
            f"G21 ; Set units to millimeters",
            f"G90 ; Absolute positioning",
            f"G1 F{self.feed_rate} ; Set feed rate",
            f
