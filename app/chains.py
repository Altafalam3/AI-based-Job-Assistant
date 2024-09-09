import os
import datetime
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: 
            `company_name`, `role`, `location`, `job_type`, `experience`, `skills`, `qualifications`, and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
            print(res, "\n\n\n")
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")

        return res if isinstance(res, list) else [res]

    def extract_resume_details(self, resume_text):
        prompt_resume = PromptTemplate.from_template(
            """
            ### RESUME TEXT:
            {resume_text}

            ### INSTRUCTION:
            Parse the provided resume text and return a structured JSON format containing the following keys: 
            `name`, `email`, `phone_number`, `address`, `education`, `skills`, `experience`, `projects`, `extra_curricular`, and `committees_and_clubs`.
            Ensure that all sections are captured accurately and concisely. The `address` field is optional and should be included only if present.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_resume = prompt_resume | self.llm
        res = chain_resume.invoke({"resume_text": resume_text})

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
            print(res, "\n\n\n")
        except OutputParserException:
            raise OutputParserException("Unable to parse resume details.")

        return res if isinstance(res, dict) else {}

    def write_cover_letter(self, job, resume_info):
        date = datetime.date.today().strftime("%B %d, %Y")
        prompt_cover_letter = PromptTemplate.from_template(
            """
            You're a cover letter writing expert. Use the details and instructions below to write a professional and tailored cover letter for a job application.

            ### JOB DESCRIPTION: (job at {company_name} for the {role} position)
            {job_description}

            ### CANDIDATE'S RESUME INFORMATION:
            Name: {name}
            Email: {email}
            Phone Number: {phone_number}
            Address: {address}
            Education: {education}
            Skills: {skills}
            Experience: {experience}
            Projects: {projects}
            Extracurricular Activities: {extra_curricular}
            Committees and Clubs: {committees_and_clubs}

            ### INSTRUCTION:
                1. Focus on the job description but don't address every point—match key job requirements with the candidate's resume.
                2. Paraphrase the details provided; do not copy directly. Present the candidate’s information in a unique and original manner.
                3. Put yourself in the reader’s shoes. What can you write that will convince the reader that you are ready and able to do the job?
                4. Keep the cover letter formal, professional, and concise, factual with no more than three paragraphs.
                5. Emphasize the candidate's most relevant skills, experience, and suitability for the role. If a skill is not listed in the provided information, then I don't have experience in it.
                6. Highlight how the candidate's background aligns with the job requirements and the company's mission.
                7. Address the letter to a specific person if possible, and tailor the tone to the organization.
                8. Avoid flowery language—use action words and give concrete examples to support qualifications.
                9. End the cover letter with a nice statement about their company reputation or why you’d like towork for them specifically and thank you.
                10. First section : Name, Address, Email, Phone number, Date : {date}.. Second section : To The hiring manager, then new line company name and address if needed.. 3rd section saluation Dear Hirin manager and then 3 paragraph of body based on above instruction .. Final section sincerely with name 
            ### COVER LETTER (NO PREAMBLE):
            """
        )

        chain_cover_letter = prompt_cover_letter | self.llm
        res = chain_cover_letter.invoke({
            "job_description": str(job),
            "company_name": job.get('company_name'),
            "role": job.get('role'),
            "name": resume_info.get('name'),
            "email": resume_info.get('email', 'No email provided.'),
            "phone_number": resume_info.get('phone_number', 'No phone number provided.'),
            "address": resume_info.get('address', 'No address provided.'),
            "education": resume_info.get('education'),
            "skills": resume_info.get('skills'),
            "experience": resume_info.get('experience'),
            "projects": resume_info.get('projects'),
            "extra_curricular": resume_info.get('extra_curricular'),
            "committees_and_clubs": resume_info.get('committees_and_clubs'),
            "date":date
        })
        return res.content

    def chat_with_llm(self, message, resume_info=None, job_info=None):
        prompt_chat = PromptTemplate.from_template(
            """
            ### USER QUESTION:
            {user_message}

            ### RESUME INFORMATION (OPTIONAL):
            {resume_info}

            ### JOB INFORMATION (OPTIONAL):
            {job_info}

            ### INSTRUCTION:
            Provide an intelligent and helpful response to the user’s query. 
            If resume and job info are provided, tailor the response based on that.
            ### RESPONSE:
            """
        )
        chain_chat = prompt_chat | self.llm
        res = chain_chat.invoke({
            "user_message": message,
            "resume_info": resume_info or "No resume info provided.",
            "job_info": job_info or "No job info provided."
        })
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
