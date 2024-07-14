from PyPDF2 import PdfReader
import re
import pickle


# Load models===========================================================================================================
rf_classifier_categorization = pickle.load(open(r'C:\Users\Dell\OneDrive\Desktop\advance web scraping\Nakri_data_set\Skill_Gap_Analysis_Tool\resume\models\rf_classifier_categorization.pkl', 'rb'))
tfidf_vectorizer_categorization = pickle.load(open(r'C:\Users\Dell\OneDrive\Desktop\advance web scraping\Nakri_data_set\Skill_Gap_Analysis_Tool\resume\models\tfidf_vectorizer_categorization.pkl', 'rb'))
rf_classifier_job_recommendation = pickle.load(open(r'C:\Users\Dell\OneDrive\Desktop\advance web scraping\Nakri_data_set\Skill_Gap_Analysis_Tool\resume\models\rf_classifier_job_recommendation.pkl', 'rb'))
tfidf_vectorizer_job_recommendation = pickle.load(open(r'C:\Users\Dell\OneDrive\Desktop\advance web scraping\Nakri_data_set\Skill_Gap_Analysis_Tool\resume\models\tfidf_vectorizer_job_recommendation.pkl', 'rb'))

# Clean resume==========================================================================================================
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

# Prediction and Category Name
def predict_category(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_categorization.transform([resume_text])
    predicted_category = rf_classifier_categorization.predict(resume_tfidf)[0]
    return predicted_category

# Prediction and Category Name
def job_recommendation(resume_text):
    resume_text= cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_job_recommendation.transform([resume_text])
    recommended_job = rf_classifier_job_recommendation.predict(resume_tfidf)[0]
    return recommended_job
# Extract text from pdf
def pdf_to_text(file):
    reader = PdfReader(file)
    text = ''
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text



def normalize_text(text):
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_contact_number_from_resume(text):

    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number
def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email

def extract_skills_from_resume(text):
    # List of predefined skills
    skills_list = [
        'Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL',
        'Tableau',
        'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'MongoDB', 'Express.js', 'Git',
        'Research', 'Statistics', 'Quantitative Analysis', 'Qualitative Analysis', 'SPSS', 'R', 'Data Visualization',
        'Matplotlib',
        'Seaborn', 'Plotly', 'Pandas', 'Numpy', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'NLTK', 'Text Mining',
        'Natural Language Processing', 'Computer Vision', 'Image Processing', 'OCR', 'Speech Recognition',
        'Recommendation Systems',
        'Collaborative Filtering', 'Content-Based Filtering', 'Reinforcement Learning', 'Neural Networks',
        'Convolutional Neural Networks',
        'Recurrent Neural Networks', 'Generative Adversarial Networks', 'XGBoost', 'Random Forest', 'Decision Trees',
        'Support Vector Machines',
        'Linear Regression', 'Logistic Regression', 'K-Means Clustering', 'Hierarchical Clustering', 'DBSCAN',
        'Association Rule Learning',
        'Apache Hadoop', 'Apache Spark', 'MapReduce', 'Hive', 'HBase', 'Apache Kafka', 'Data Warehousing', 'ETL',
        'Big Data Analytics',
        'Cloud Computing', 'Amazon Web Services (AWS)', 'Microsoft Azure', 'Google Cloud Platform (GCP)', 'Docker',
        'Kubernetes', 'Linux',
        'Shell Scripting', 'Cybersecurity', 'Network Security', 'Penetration Testing', 'Firewalls', 'Encryption',
        'Malware Analysis',
        'Digital Forensics', 'CI/CD', 'DevOps', 'Agile Methodology', 'Scrum', 'Kanban', 'Continuous Integration',
        'Continuous Deployment',
        'Software Development', 'Web Development', 'Mobile Development', 'Backend Development', 'Frontend Development',
        'Full-Stack Development',
        'UI/UX Design', 'Responsive Design', 'Wireframing', 'Prototyping', 'User Testing', 'Adobe Creative Suite',
        'Photoshop', 'Illustrator',
        'InDesign', 'Figma', 'Sketch', 'Zeplin', 'InVision', 'Product Management', 'Market Research',
        'Customer Development', 'Lean Startup',
        'Business Development', 'Sales', 'Marketing', 'Content Marketing', 'Social Media Marketing', 'Email Marketing',
        'SEO', 'SEM', 'PPC',
        'Google Analytics', 'Facebook Ads', 'LinkedIn Ads', 'Lead Generation', 'Customer Relationship Management (CRM)',
        'Salesforce',
        'HubSpot', 'Zendesk', 'Intercom', 'Customer Support', 'Technical Support', 'Troubleshooting',
        'Ticketing Systems', 'ServiceNow',
        'ITIL', 'Quality Assurance', 'Manual Testing', 'Automated Testing', 'Selenium', 'JUnit', 'Load Testing',
        'Performance Testing',
        'Regression Testing', 'Black Box Testing', 'White Box Testing', 'API Testing', 'Mobile Testing',
        'Usability Testing', 'Accessibility Testing',
        'Cross-Browser Testing', 'Agile Testing', 'User Acceptance Testing', 'Software Documentation',
        'Technical Writing', 'Copywriting',
        'Editing', 'Proofreading', 'Content Management Systems (CMS)','Word', 'Excel', 'PowerPoint', 'WordPress', 'Joomla', 'Drupal', 'Magento',
        'Shopify', 'E-commerce',
        'Payment Gateways', 'Inventory Management', 'Supply Chain Management', 'Logistics', 'Procurement',
        'ERP Systems', 'SAP', 'Oracle',
        'Microsoft Dynamics', 'Tableau', 'Power BI', 'QlikView', 'Looker', 'Data Warehousing', 'ETL',
        'Data Engineering', 'Data Governance',
        'Data Quality', 'Master Data Management', 'Predictive Analytics', 'Prescriptive Analytics',
        'Descriptive Analytics', 'Business Intelligence',
        'Dashboarding', 'Reporting', 'Data Mining', 'Web Scraping', 'API Integration', 'RESTful APIs', 'GraphQL',
        'SOAP', 'Microservices',
        'Serverless Architecture', 'Lambda Functions', 'Event-Driven Architecture', 'Message Queues','Manupatra', 'SCC Online', 'GraphQL',
        'Socket.io', 'WebSockets'
                     'Ruby', 'Ruby on Rails', 'PHP', 'Symfony', 'Laravel', 'CakePHP', 'Zend Framework', 'ASP.NET', 'C#',
        'VB.NET', 'ASP.NET MVC', 'Entity Framework',
        'Spring', 'Hibernate', 'Struts', 'Kotlin', 'Swift', 'Objective-C', 'iOS Development', 'Android Development',
        'Flutter', 'React Native', 'Ionic',
        'Mobile UI/UX Design', 'Material Design', 'SwiftUI', 'RxJava', 'RxSwift', 'Django', 'Flask', 'FastAPI',
        'Falcon', 'Tornado', 'WebSockets',
        'GraphQL', 'RESTful Web Services', 'SOAP', 'Microservices Architecture', 'Serverless Computing', 'AWS Lambda',
        'Google Cloud Functions',
        'Azure Functions', 'Server Administration', 'System Administration', 'Network Administration',
        'Database Administration', 'MySQL', 'PostgreSQL',
        'SQLite', 'Microsoft SQL Server', 'Oracle Database', 'NoSQL', 'MongoDB', 'Cassandra', 'Redis', 'Elasticsearch',
        'Firebase', 'Google Analytics',
        'Google Tag Manager', 'Adobe Analytics', 'Marketing Automation', 'Customer Data Platforms', 'Segment',
        'Salesforce Marketing Cloud', 'HubSpot CRM',
        'Zapier', 'IFTTT', 'Workflow Automation', 'Robotic Process Automation (RPA)', 'UI Automation',
        'Natural Language Generation (NLG)',
        'Virtual Reality (VR)', 'Augmented Reality (AR)', 'Mixed Reality (MR)', 'Unity', 'Unreal Engine', '3D Modeling',
        'Animation', 'Motion Graphics',
        'Game Design', 'Game Development', 'Level Design', 'Unity3D', 'Unreal Engine 4', 'Blender', 'Maya',
        'Adobe After Effects', 'Adobe Premiere Pro',
        'Final Cut Pro', 'Video Editing', 'Audio Editing', 'Sound Design', 'Music Production', 'Digital Marketing',
        'Content Strategy', 'Conversion Rate Optimization (CRO)',
        'A/B Testing', 'Customer Experience (CX)', 'User Experience (UX)', 'User Interface (UI)', 'Persona Development',
        'User Journey Mapping', 'Information Architecture (IA)',
        'Wireframing', 'Prototyping', 'Usability Testing', 'Accessibility Compliance', 'Internationalization (I18n)',
        'Localization (L10n)', 'Voice User Interface (VUI)',
        'Chatbots', 'Natural Language Understanding (NLU)', 'Speech Synthesis', 'Emotion Detection',
        'Sentiment Analysis', 'Image Recognition', 'Object Detection',
        'Facial Recognition', 'Gesture Recognition', 'Document Recognition', 'Fraud Detection',
        'Cyber Threat Intelligence', 'Security Information and Event Management (SIEM)',
        'Vulnerability Assessment', 'Incident Response', 'Forensic Analysis', 'Security Operations Center (SOC)',
        'Identity and Access Management (IAM)', 'Single Sign-On (SSO)',
        'Multi-Factor Authentication (MFA)', 'Blockchain', 'Cryptocurrency', 'Decentralized Finance (DeFi)',
        'Smart Contracts', 'Web3', 'Non-Fungible Tokens (NFTs)']


    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills

def extract_education_from_resume(text):
    education = []

    # List of education keywords to match against
    education_keywords = [
        'Computer Science', 'Information Technology', 'Software Engineering', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering',
        'Chemical Engineering', 'Biomedical Engineering', 'Aerospace Engineering', 'Nuclear Engineering', 'Industrial Engineering', 'Systems Engineering',
        'Environmental Engineering', 'Petroleum Engineering', 'Geological Engineering', 'Marine Engineering', 'Robotics Engineering', 'Biotechnology',
        'Biochemistry', 'Microbiology', 'Genetics', 'Molecular Biology', 'Bioinformatics', 'Neuroscience', 'Biophysics', 'Biostatistics', 'Pharmacology',
        'Physiology', 'Anatomy', 'Pathology', 'Immunology', 'Epidemiology', 'Public Health', 'Health Administration', 'Nursing', 'Medicine', 'Dentistry',
        'Pharmacy', 'Veterinary Medicine', 'Medical Technology', 'Radiography', 'Physical Therapy', 'Occupational Therapy', 'Speech Therapy', 'Nutrition',
        'Sports Science', 'Kinesiology', 'Exercise Physiology', 'Sports Medicine', 'Rehabilitation Science', 'Psychology', 'Counseling', 'Social Work',
        'Sociology', 'Anthropology', 'Criminal Justice', 'Political Science', 'International Relations', 'Economics', 'Finance', 'Accounting', 'Business Administration',
        'Management', 'Marketing', 'Entrepreneurship', 'Hospitality Management', 'Tourism Management', 'Supply Chain Management', 'Logistics Management',
        'Operations Management', 'Human Resource Management', 'Organizational Behavior', 'Project Management', 'Quality Management', 'Risk Management',
        'Strategic Management', 'Public Administration', 'Urban Planning', 'Architecture', 'Interior Design', 'Landscape Architecture', 'Fine Arts',
        'Visual Arts', 'Graphic Design', 'Fashion Design', 'Industrial Design', 'Product Design', 'Animation', 'Film Studies', 'Media Studies',
        'Communication Studies', 'Journalism', 'Broadcasting', 'Creative Writing', 'English Literature', 'Linguistics', 'Translation Studies',
        'Foreign Languages', 'Modern Languages', 'Classical Studies', 'History', 'Archaeology', 'Philosophy', 'Theology', 'Religious Studies',
        'Ethics', 'Education', 'Early Childhood Education', 'Elementary Education', 'Secondary Education', 'Special Education', 'Higher Education',
        'Adult Education', 'Distance Education', 'Online Education', 'Instructional Design', 'Curriculum Development', 'Library Science', 'Information Science',
        'Computer Engineering', 'Software Development', 'Cybersecurity', 'Information Security', 'Network Engineering', 'Data Science', 'Data Analytics',
        'Business Analytics', 'Operations Research', 'Decision Sciences', 'Human-Computer Interaction', 'User Experience Design', 'User Interface Design',
        'Digital Marketing', 'Content Strategy', 'Brand Management', 'Public Relations', 'Corporate Communications', 'Media Production', 'Digital Media',
        'Web Development', 'Mobile App Development', 'Game Development', 'Virtual Reality', 'Augmented Reality', 'Blockchain Technology', 'Cryptocurrency',
        'Digital Forensics', 'Forensic Science', 'Criminalistics', 'Crime Scene Investigation', 'Emergency Management', 'Fire Science', 'Environmental Science',
        'Climate Science', 'Meteorology', 'Geography', 'Geomatics', 'Remote Sensing', 'Geoinformatics', 'Cartography', 'GIS (Geographic Information Systems)',
        'Environmental Management', 'Sustainability Studies', 'Renewable Energy', 'Green Technology', 'Ecology', 'Conservation Biology', 'Wildlife Biology',
        'Zoology'
    ]

    # Add common degree abbreviations and formats
    degree_keywords = [
        'Bachelor of', 'Master of', 'B.Sc', 'M.Sc', 'B.Tech', 'M.Tech', 'B.E.', 'M.E.', 'BBA', 'MBA', 'BCA', 'MCA', 'Ph.D', 'Doctorate', 'Diploma'
    ]

    combined_keywords = education_keywords + degree_keywords

    # Clean and normalize the text
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space

    # Patterns to capture educational details
    patterns = [
        r'(?i)\b(?:' + '|'.join(map(re.escape, combined_keywords)) + r')\b.*?(?=\s+\d{4}|$)',
        r'(?i)\b(?:Spring|Summer|Fall|Winter)\b \d{4}',
        r'(?i)\b\d{4}\b'
    ]
    # 0681810061

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            education.append(match.strip())

    # Post-process to clean the extracted data
    processed_education = []
    for item in education:
        if any(kw.lower() in item.lower() for kw in combined_keywords) and re.search(r'\d{4}', item):
            processed_education.append(item)
    
    return list(set(processed_education))  # Remove duplicates


def extract_soft_skill(text):
    softskill = []

    softskill_keyword  =["Adaptability", "Analytical Thinking", "Attention to Detail", "Collaboration", 
    "Communication", "Conflict Resolution", "Creativity", "Critical Thinking", 
    "Decision Making", "Emotional Intelligence", "Empathy", "Flexibility", 
    "Interpersonal Skills", "Leadership", "Listening", "Negotiation", "Networking", 
    "Open-Mindedness", "Organization", "Patience", "Persuasion", "Problem Solving", 
    "Public Speaking", "Resourcefulness", "Self-Motivation", "Teamwork", "Time Management", 
    "Work Ethic", "Positive Attitude", "Stress Management", "Resilience", "Initiative", 
    "Adaptability", "Collaboration", "Integrity", "Multitasking", "Dependability", 
    "Dedication", "Determination", "Discipline", "Energy", "Innovation", "Insight", 
    "Enthusiasm", "Honesty", "Influencing", "Optimism", "Perseverance", "Proactivity", 
    "Professionalism", "Punctuality", "Respectfulness", "Responsibility", "Self-Awareness", 
    "Self-Confidence", "Self-Discipline", "Self-Management", "Strategic Thinking", 
    "Tactfulness", "Tenacity", "Thoroughness", "Trustworthiness", "Work Under Pressure", 
    "Adaptability to Change", "Assertiveness", "Business Acumen", "Client Management", 
    "Coaching", "Competitiveness", "Computer Literacy", "Continuous Improvement", 
    "Cultural Awareness", "Customer Service", "Delegation", "Detail Orientation", 
    "Diplomacy", "Diversity Awareness", "Event Planning", "Facilitation", "Follow-Through", 
    "Goal Setting", "Independence", "Influence", "Initiative", "Innovation Management", 
    "Intuition", "Judgment", "Logical Thinking", "Market Awareness", "Mentoring", 
    "Motivating Others", "Negotiating Skills", "Nonverbal Communication", "Objective Thinking", 
    "Oral Communication", "Organization Skills", "People Skills", "Performance Management", 
    "Personal Accountability", "Persuasiveness", "Planning", "Prioritization", "Project Management", 
    "Providing Feedback", "Reading Body Language", "Relationship Building", "Results Orientation", 
    "Risk Management", "Scheduling", "Self-Assessment", "Self-Critique", "Selling Skills", 
    "Sensitivity", "Service Orientation", "Situational Awareness", "Social Intelligence", 
    "Stakeholder Management", "Storytelling", "Supervision", "Systems Thinking", 
    "Talent Management", "Task Management", "Technical Writing", "Training", 
    "Verbal Communication", "Visual Communication", "Volunteer Management", "Work Ethic", 
    "Written Communication", "Adaptability to New Technology", "Assertive Communication", 
    "Awareness of Others", "Benchmarking", "Brand Management", "Business Development", 
    "Client Relations", "Collaborative Problem Solving", "Competitive Analysis", "Conceptual Thinking", 
    "Conflict Management", "Consensus Building", "Constructive Criticism", "Consulting", 
    "Contract Negotiation", "Cost Control", "Creative Thinking", "Crisis Management", 
    "Customer Retention", "Customer Relationship Management", "Data Analysis", "Data Interpretation", 
    "Data Presentation", "Decision-Making Skills", "Emotional Regulation", "Empowering Others", 
    "Endurance", "Ethical Judgment", "Event Coordination", "Executive Presence", "Facilitating Discussions", 
    "Financial Acumen", "Forecasting", "Global Mindset", "Goal Achievement", "Group Dynamics", 
    "Growth Mindset", "Influence and Persuasion", "Information Management", "Initiating Action", 
    "Intellectual Curiosity", "Intercultural Communication", "Interdisciplinary Approach", 
    "Knowledge Sharing", "Leadership Development", "Learning Agility", "Listening Skills", 
    "Managing Ambiguity", "Managing Expectations", "Managing Upwards", "Meeting Facilitation", 
    "Mentorship", "Multi-Cultural Competence", "Networking Skills", "Organizational Agility", 
    "Performance Improvement", "Personal Branding", "Persuasive Communication", "Presentation Skills", 
    "Prioritizing Tasks", "Process Improvement", "Professional Networking", "Public Relations", 
    "Quality Focus", "Reflective Practice", "Resilient Leadership", "Respect for Diversity", 
    "Scenario Planning", "Self-Reflection", "Service Excellence", "Situational Leadership", 
    "Social Media Literacy", "Stakeholder Engagement", "Strategic Leadership", "Sustainability Awareness", 
    "Talent Development", "Team Development", "Technical Communication", "Transformational Leadership", 
    "User Experience Awareness", "Virtual Collaboration", "Visionary Thinking", "Wellness Management", 
    "Work-Life Balance"
]
 # Join keywords into a single pattern, separated by "|"
    pattern = r"\b(?:{})\b".format("|".join(re.escape(keyword) for keyword in softskill_keyword))
    matches = re.findall(pattern, text, re.IGNORECASE)
    softskill = list(set(matches))  # Remove duplicates if any

    print("Pattern:", pattern)  # Debug print to see the pattern
    print("Matches:", matches)  # Debug print to see the matches

    return softskill

def extract_name_from_resume(text):
    name = None

    # Use regex pattern to find a potential name
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()

    return name
def extract_location_from_resume(text):
    name = None

    # Use regex pattern to find a potential location
    pattern = r'\b[A-Za-z]+\s*,\s*[A-Za-z]+\b'
    match = re.search(pattern, text)
    if match:
        location = match.group()

    return location

resume = r'C:\Users\Dell\OneDrive\Desktop\advance web scraping\Nakri_data_set\Skill_Gap_Analysis_Tool\resume\data\fresher_1_page_resume.pdf'


def pred(resume_file):
    # Process the PDF file and make predictions
    if resume_file.endswith('.pdf'):
        text = pdf_to_text(resume_file)
    else:
        return "Invalid file format. Please upload a PDF file."

    print("Resume Text:", text)  # Debug print to see the resume text

    # Predict category and job recommendation
    predicted_category = predict_category(text)
    recommended_job = job_recommendation(text)

    # Extract contact information
    phone = extract_contact_number_from_resume(text)
    email = extract_email_from_resume(text)

    # Extract skills, soft skills, education, and name
    extracted_skills = extract_skills_from_resume(text)
    extracted_softskills = extract_soft_skill(text)
    extracted_education = extract_education_from_resume(text)
    name = extract_name_from_resume(text)

    # Print or return the extracted information
    print("Predicted Category:", predicted_category)
    print("Recommended Job:", recommended_job)
    print("Contact Number:", phone)
    print("Email:", email)
    print("Extracted Skills:", extracted_skills)
    print("Extracted Soft Skills:", extracted_softskills)
    print("Extracted Education:", extracted_education)
    print("Name:", name)

    return {
        "predicted_category": predicted_category,
        "recommended_job": recommended_job,
        "contact_number": phone,
        "email": email,
        "skills": extracted_skills,
        "soft_skills": extracted_softskills,
        "education": extracted_education,
        "name": name
    }

print(pred(resume))