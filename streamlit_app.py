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
    reader = easyocr.Reader(['en', 'es'])
    image = Image.open(uploaded_file)
    image = image.convert("RGB")
    image_np = np.array(image)

    result = reader.readtext(image_np)
    for detection in result:
        text=detection[1]
        bbox = detection[0]
        st.write(f'Text:{text}')



