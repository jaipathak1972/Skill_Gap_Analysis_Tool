from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google Generative AI
genai.configure(api_key=os.getenv("API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path=r"C:\Users\Dell\OneDrive\Desktop\poppler-24.02.0\Library\bin")

        # Get the first page
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
# submit2 = st.button("Extract education")
# submit3 = st.button("Percentage Match")
submit4 = st.button("Extract Name")
submit5 = st.button("Extract Location")
submit6 = st.button("Extract Experience")

input_prompt1 = """You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. Your task is to extract all TECHNICAL SKILLS from the provided resume. 
List the top 10 to 30 skills mentioned in the resume.Only technical skills remember that and try to give minimum 
"""
# input_prompt2 = """You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality Extract ACADEMIC QUALIFICATIONS of the candidate from the resume latest if not founded then say dont have education

# """
input_prompt4 = """You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality Extract NAME of the candidate from the resume latest if not founded then say dont have education

"""
input_prompt5 = """You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality Extract LOCATION of the candidate from the resume latest if not founded then say dont have Location

"""
input_prompt6 = """You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality Extract Experience of the candidate from the resume latest if not founded then say Fresher

"""

# input_prompt3 = """
# You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
# Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
# the job description. First, the output should come as percentage, then keywords missing, and lastly final thoughts.
# """

Resume_Data = {}

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
        Resume_Data["Skill":response]
    else:
        st.write("Please upload the resume")

# elif submit2:
#     if uploaded_file is not None:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_text, pdf_content, input_prompt2)
#         st.subheader("The Response is")
#         st.write(response)
#         Resume_Data["Skill":response]

        
#     else:
#         st.write("Please upload the resume")

# elif submit3:
#     if uploaded_file is not None:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_text, pdf_content, input_prompt3)
#         st.subheader("The Response is")
#         st.write(response)
#         Resume_Data["Percentage":response]
        
#     else:
#         st.write("Please upload the resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt4)
        st.subheader("The Response is")
        st.write(response)
        Resume_Data["Name":response]

    else:
        st.write("Please upload the resume")
elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt5)
        st.subheader("The Response is")
        st.write(response)
        Resume_Data["Location":response]

    else:
        st.write("Please upload the resume")
elif submit6:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt6)
        st.subheader("The Response is")
        st.write(response)
        Resume_Data["Expirence":response]

    else:
        st.write("Please upload the resume")

