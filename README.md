# 📧 AI Based Job Assistant

## Overview

Job seekers often face the overwhelming task of crafting tailored resumes and cover letters for each job application. This process is not only time-consuming but can also become mentally exhausting, especially when juggling multiple applications simultaneously. The repetitive nature of customizing documents to fit specific job descriptions, adjusting tone and style to suit different companies, and dealing with the pressure to make a strong impression can lead to burnout and reduced productivity.

Additionally, the emotional strain of the job search process, compounded by rejection and uncertainty, can negatively impact mental health. Many individuals, particularly students or early-career professionals, may feel isolated or overwhelmed, finding it difficult to seek guidance from mentors or share their thoughts with others.

## Features

The **AI-Driven Job Application Assistant** is designed to address these challenges by offering:

- **Automated Tailored Cover Letters:** 
  A personalized tool that automatically generates tailored cover letters for specific job applications. The cover letter is provided in an editable format and can be downloaded directly by the user, eliminating the need to switch between platforms or manually copy and paste text elsewhere.

- **Resume Matching with Job Descriptions:** 
  The tool extracts key details from job links and matches them with the user's resume. It suggests updates and improvements to help users align their resumes more effectively with job requirements.

- **Chatbot:** 
  A chatbot feature that provides emotional support, advice based on the resume or job destriction. It helps users navigate the mental challenges of job hunting.

## Demo

![image](https://github.com/user-attachments/assets/999f96b4-7070-49e0-9881-2dd6516b5157)
![image1](https://github.com/user-attachments/assets/4564fbeb-00bd-43b3-8165-eb3171f401f5)
![image2](https://github.com/user-attachments/assets/a8bb84a6-ed5c-4e40-8f2c-132623d8f90e)
![image3](https://github.com/user-attachments/assets/b6cf53c8-0efe-4202-a160-437dd93554c8)
![image4](https://github.com/user-attachments/assets/746db7bc-c836-48fe-a966-9cf5c6839c4e)
![image5](https://github.com/user-attachments/assets/b397122b-ba6d-4554-8585-f21dee90bf0a)




## Goals

This solution aims to:
- Streamline the job application process.
- Provide tools that make the entire process more manageable and efficient, reducing stress and improving productivity.

## Getting Started

1. **Tailored Cover Letters:** Input the job description and your resume details. The tool will automatically generate a cover letter, which you can edit and download in one place.

2. **Resume Matching:** Upload your resume and provide the job link. The tool will extract details from the job listing and match it with your resume, suggesting necessary updates.

3. **Chatbot Support:** Use the chatbot for advice or emotional support during the job search process.

## Future Improvements

- Enhanced AI suggestions for resume and cover letter improvements.
- Integration with job boards for easier job application management.
- Expanded mental health resources within the chatbot feature.


## Set-up

1. To get started we first need to get an API_KEY from here: https://console.groq.com/keys. Inside `app/.env` update the value of `GROQ_API_KEY` with the API_KEY you created.

2. To get started, first install the dependencies using:
   ```commandline
    pip install -r requirements.txt
   ```
3. Run the streamlit app:
   ```commandline
   streamlit run app/main.py
   ```

4. Run the streamlit app:
   ```commandline
   streamlit run app/chatbot.py
   ```

