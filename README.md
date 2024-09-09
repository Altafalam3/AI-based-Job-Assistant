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

- **Tone Flexibility:** 
  Offers flexibility in crafting cover letters with varying tones, from highly professional to more conversational, depending on the target recipient (e.g., formal for companies, informal for alumni or mentors).

- **Emotional Support Chatbot:** 
  A chatbot feature that provides emotional support, advice, and a space to vent during the stressful job search process. It helps users navigate the mental challenges of job hunting.

## Goals

This solution aims to:
- Streamline the job application process.
- Offer mental health support to job seekers.
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

