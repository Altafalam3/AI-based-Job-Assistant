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
        prompt_cover_letter = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
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
            Write a formal professional cover letter for the candidate applying to the job at {company_name} for the {role} position. 
            The cover letter should be professional and emphasize the candidate's skills, experience, and suitability for the role. 
            Mention how the candidate's background aligns with the job requirements and the company's mission.
            Maintain a formal tone and structure.

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
            "committees_and_clubs": resume_info.get('committees_and_clubs')
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
