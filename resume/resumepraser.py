# Import libraries
import yaml
from google.generativeai import configure, GenerativeModel

# Configure the generative AI model
configure(api_key='AIzaSyC-xdiuimQ3-_Bn8QrFt55Ynnl-')
model = GenerativeModel("gemini-pro")

def ats_extractor(resume_data):
    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes. You are given a resume and your job is to extract the following information from the resume:
    1. full name
    2. email id
    3. github portfolio
    4. linkedin id
    5. employment details
    6. technical skills
    7. soft skills
    Give the extracted information in json format only.
    '''

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": resume_data}
    ]

    response = model.chat(
        messages=messages,
        temperature=0.0,
        max_tokens=1500
    )
    
    data = response['choices'][0]['message']['content']
    
    return data
