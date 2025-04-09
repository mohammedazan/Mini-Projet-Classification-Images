from sklearn.svm import SVC
import numpy as np
from PIL import Image
import os

class ImageClassifier:
    def __init__(self):
        self.model = SVC(probability=True)
        self.image_size = (150, 150)
        
    def preprocess_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize(self.image_size)
        img = img.convert('RGB')  # Ensure RGB format
        img_array = np.array(img)
        # Flatten the image array
        return img_array.reshape(1, -1)[0]

    def train(self, cat_images, dog_images):
        # Prepare training data
        X = []
        y = []
        
        for img_path in cat_images:
            X.append(self.preprocess_image(img_path))
            y.append(0)  # 0 for cats
            
        for img_path in dog_images:
            X.append(self.preprocess_image(img_path))
            y.append(1)  # 1 for dogs
            
        X = np.array(X)
        y = np.array(y)
        
        # Train the model
        self.model.fit(X, y)

    def predict(self, image_path):
        img = self.preprocess_image(image_path)
        img = img.reshape(1, -1)
        
        prediction = self.model.predict(img)[0]
        probabilities = self.model.predict_proba(img)[0]
        
        # Convert prediction to label and confidence
        label = "Dog" if prediction == 1 else "Cat"
        confidence = probabilities[1] if prediction == 1 else probabilities[0]
        
        return label, confidence * 100