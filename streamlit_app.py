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

