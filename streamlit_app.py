import easyocr
from PIL import Image
import streamlit as st
import numpy as np
import io

# Define the containers for Streamlit layout
header = st.container()
data = st.container()
features = st.container()
modelTraining = st.container()



# Header section for the Streamlit app
with header:
    st.title('Let\'s Scan a Business Card')

# File uploader for image input
uploaded_file = st.file_uploader("Upload a business card image for OCR analysis", type=["jpg", "jpeg", "png", "bmp"])
