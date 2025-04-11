import torch
import torchvision.transforms as transforms
from PIL import Image
import logging
import os
import sys

def setup_logger():
    logger = logging.getLogger('MLModule')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('ml_module.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

class MaterialClassifier:
    def __init__(self, model_path='material_classifier.pth'):
        self.model_path = model_path
        self.model = self.load_model()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

    def load_model(self):
        logger.info(f"Loading model from {self.model_path}.")
        if not os.path.exists(self.model_path):
            logger.error(f"Model file {self.model_path} not found.")
            raise FileNotFoundError(f"Model file {self.model_path} not found.")
        model = torch.load(self.model_path, map_location=torch.device('cpu'))
        model.eval()
        logger.info("Model loaded successfully.")
        return model

    def predict(self, image_path):
        logger.info(f"Predicting material for image {image_path}.")
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            output = self.model(input_tensor)
            predicted_class = output.argmax(dim=1).item()
        logger.info(f"Predicted class: {predicted_class}")
        return predicted_class

def main():
    try:
        classifier = MaterialClassifier()
        test_image = 'captured_images/sample.png'  # Replace with actual image path
        prediction = classifier.predict(test_image)
        logger.info(f"Material prediction: {prediction}")
    except Exception as e:
        logger.exception("An error occurred in the ML module.")
        sys.exit(1)

if __name__ == '__main__':
    main()
