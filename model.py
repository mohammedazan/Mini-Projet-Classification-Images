from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np
from PIL import Image
import os
import cv2

class ImageClassifier:
    def __init__(self):
        self.model = SVC(kernel='rbf', probability=True)
        self.scaler = StandardScaler()
        
    def extract_features(self, image_path):
        # Load and resize image
        img = cv2.imread(image_path)
        img = cv2.resize(img, (128, 128))  # Larger size for better features
        
        # Extract more robust features
        features = []
        
        # Add color features
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        features.extend(np.mean(hsv, axis=(0,1)))
        
        # Add HOG features
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hog = cv2.HOGDescriptor()
        features.extend(hog.compute(gray).flatten())
        
        return np.array(features)

    def train(self, cat_images, dog_images):
        X = []
        y = []
        
        # Process cat images
        for img_path in cat_images:
            features = self.extract_features(img_path)
            X.append(features)
            y.append('chat')
            
        # Process dog images
        for img_path in dog_images:
            features = self.extract_features(img_path)
            X.append(features)
            y.append('chien')
        
        # Scale features
        X = self.scaler.fit_transform(X)
        
        # Train model with better parameters
        self.model = SVC(kernel='rbf', C=10, gamma='scale', probability=True)
        self.model.fit(X, y)

    def predict(self, image_path):
        # Extract and scale features
        features = self.extract_features(image_path)
        features = self.scaler.transform(features.reshape(1, -1))
        
        # Get prediction and probability
        prediction = self.model.predict(features)[0]
        proba = self.model.predict_proba(features)[0]
        confidence = max(proba) * 100
        
        return prediction, confidence