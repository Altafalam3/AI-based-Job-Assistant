# 📧 AI Based Job Assistant

It’s like having a personal advisor who helps you with the whole process. It will help you adjust your resume for specific jobs, and even create cover letters that match the tone you need. For example, if you’re sending a cover letter to a company, it can make it sound very professional. But if you’re reaching out to a senior or alumni, it can be more conversational.
This feature is designed to take a huge load off your shoulders, because preparing cover letter for every company is very tiring process

For ME AND many of us, the whole process can become overwhelming, to the point where it affects our mental health. Sometimes, you just need someone to talk to, but it’s not always easy to share your thoughts with mentors or teachers. That’s why we’re including a chatbot feature in CAREERLINK—a space where you can vent your feelings, seek advice, or just get some supportive words when you need them the most. This feature is designed to help you navigate those tough moments, so you don’t have to carry the burden alone.

## Architecture Diagram

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

