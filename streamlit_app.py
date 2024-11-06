import easyocr
import streamlit as st

header = st.container()
data = st.container()
features = st.container()
modelTraining = st.container()

with header:
        st.title('lets scan a business card')
        
        
uploaded_file = st.file_uploader("upload a csv file for analysis")

if uploaded_file is not None:
    st.title('lets scan a business card 2')

