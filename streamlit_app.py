import easyocr
import streamlit as st

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

if uploaded_file is not None:
    # Initialize EasyOCR reader for English and Spanish
    reader = easyocr.Reader(['en', 'es'])

    # Convert the uploaded file into a byte stream and then open as a PIL image
    image = Image.open(io.BytesIO(uploaded_file.read()))
    image = image.convert("RGB")  # Ensure the image is in RGB format

    # Convert the PIL image to a numpy array
    image_np = np.array(image)

    # Perform OCR with EasyOCR
    result = reader.readtext(image_np)

    # Display detected text and bounding boxes in Streamlit
    st.write("Detected Text from the business card:")
    for detection in result:
        text = detection[1]  # Extract the detected text
        bbox = detection[0]  # Extract the bounding box coordinates (optional)
        st.write(f'Text: {text}')
        st.write(f'Bounding Box: {bbox}')  # You can also show the bounding box if needed

