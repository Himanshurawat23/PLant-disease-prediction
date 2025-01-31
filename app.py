from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini AI API with the correct environment variable
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get response from Gemini API
def get_gemini_response(input, image):
    try:
        response = model.generate_content([input, image[0]])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Convert uploaded image into bytes
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="MultiLanguage Disease Predictor")
st.header("Plant Disease Predictor")

# Input fields for the prompt and file uploader
# input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Drop the plant Image")

# Pre-defined input prompt
input_prompt = """
You are an expert in understanding the plant disease . We will upload an image of plant, 
and your response contains the name of the disease and suggests how to cure the disease give the response in structured manner.
"""

# Submit button logic
if submit:
    try:
        with st.spinner("Processing..."):
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            st.subheader("The Response is:")
            st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
