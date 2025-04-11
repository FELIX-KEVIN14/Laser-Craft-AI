import cv2
import os
import sys
import argparse
import logging
from datetime import datetime

def setup_logger():
    logger = logging.getLogger('InputModule')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('input_module.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

def capture_image(camera_index=0, save_path='captured_images'):
    logger.info("Starting image capture.")
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        logger.error("Cannot open camera.")
        raise IOError("Cannot open camera.")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        logger.error("Failed to capture image.")
        raise IOError("Failed to capture image.")
    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'image_{timestamp}.png'
    filepath = os.path.join(save_path, filename)
    cv2.imwrite(filepath, frame)
    logger.info(f"Image saved to {filepath}.")
    return filepath

def get_user_input():
    logger.info("Collecting user input.")
    parser = argparse.ArgumentParser(description='Laser Cutting Input Module')
    parser.add_argument('--shape', type=str, required=True, help='Shape to cut (e.g., circle, square)')
    parser.add_argument('--size', type=float, required=True, help='Size parameter for the shape')
    args = parser.parse_args()
    logger.info(f"User input: shape={args.shape}, size={args.size}")
    return args.shape, args.size

def main():
    try:
        shape, size = get_user_input()
        image_path = capture_image()
        logger.info(f"Captured image at {image_path} for shape {shape} with size {size}.")
    except Exception as e:
        logger.exception("An error occurred in the input module.")
        sys.exit(1)

if __name__ == '__main__':
    main()
