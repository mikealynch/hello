import os
import easyocr
import streamlit as st
from PIL import Image
import numpy as np
import io
import torch
import cv2

# Set the environment variable before importing easyocr
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

header = st.container()
data = st.container()
features = st.container()
modelTraining = st.container()

# Header section for the Streamlit app
with header:
    st.title('Let\'s Scan a Business Card')

# File uploader for image input
uploaded_file = st.file_uploader("Upload a business card image for OCR analysis", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    try:
        # Debugging: Print the type of the uploaded file to ensure it's correct
        st.write(f"Uploaded file type: {uploaded_file.type}")
        
        # Step 1: Convert the uploaded file to a NumPy array (OpenCV format)
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Decode into OpenCV image format

        if image is None:
            raise ValueError("Failed to load image. Ensure the file is a valid image.")

        # Step 2: Convert the image to HSV color space for color-based segmentation
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Step 3: Define color range for segmentation (adjust these ranges based on card's color)
        lower_bound = np.array([0, 0, 180])   # Light color lower HSV bound
        upper_bound = np.array([180, 50, 255])  # Light color upper HSV bound

        # Step 4: Create a mask for colors within the specified range
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        # Step 5: Find contours based on the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise ValueError("No contours found; make sure the color range includes the business card.")
            
        # Step 6: Find the largest contour, assume it’s the business card
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Step 7: Apply padding to include a bit more of the card's edges
        x = max(0, x)
        y = max(0, y)
        w = min(image.shape[1] - x, w + 2)
        h = min(image.shape[0] - y, h + 2)

        # Step 8: Crop the image to the expanded bounding box
        cropped_image = image[y:y+h, x:x+w]

        # Step 9: Convert to Pillow image for saving without compression
        pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        
        # Display the cropped image in Streamlit
        st.image(pil_image, caption="Cropped Business Card", use_column_width=True)

        # Initialize EasyOCR reader for English and Spanish
        reader = easyocr.Reader(['en', 'es'])

        # Convert the cropped image into a numpy array
        image_np = np.array(pil_image)

        # Perform OCR with EasyOCR
        result = reader.readtext(image_np)

        # Display detected text and bounding boxes in Streamlit
        st.write("Detected Text from the business card:")
        for detection in result:
            text = detection[1]  # Extract the detected text
            bbox = detection[0]  # Extract the bounding box coordinates (optional)
            st.write(f'Text: {text}')
            #st.write(f'Bounding Box: {bbox}')  # You can also show the bounding box if needed
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
