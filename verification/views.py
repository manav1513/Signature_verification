from django.shortcuts import render
from django.http import JsonResponse
from .models import Signature
import cv2
import numpy as np
import tensorflow as tf
import os
# Load the saved model
model = tf.keras.models.load_model(os.path.join('media', 'bi_rnn_signature_verification_model.h5'))

# Function to preprocess a single input image
def preprocess_image(image_path, img_size=(256, 256)):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    img = cv2.resize(img, img_size)
    img = img / 255.0  # Normalize the image
    img = img.reshape(1, img_size[0] * img_size[1])  # Flatten
    return img

# Function to predict and return result
def verify_signature(image_path):
    try:
        # Preprocess the image
        image = preprocess_image(image_path)

        # Make prediction
        prediction = model.predict(image)

        # Determine the result
        result = np.argmax(prediction)
        confidence = np.max(prediction)

        # True for genuine, False for forged
        return True if result == 0 else False, confidence
    except Exception as e:
        print(f"Error in processing: {e}")
        return None, None

def upload_signature(request):
    is_genuine = None
    confidence = None
    signature_id = None
    if request.method == 'POST' and request.FILES.get('signature_image'):
        # Handle the uploaded signature image
        signature_image = request.FILES['signature_image']
        signature_instance = Signature.objects.create(image=signature_image)

        # Save the image to a temporary location
        with open('uploaded_signature.png', 'wb') as f:
            for chunk in signature_image.chunks():
                f.write(chunk)

        # Verify the signature
        is_genuine, confidence = verify_signature('uploaded_signature.png')
        signature_id = signature_instance.id

    return render(request, 'verification/upload_signature.html', {
        'is_genuine': is_genuine,
        'confidence': confidence,
        'signature_id': signature_id
    })
