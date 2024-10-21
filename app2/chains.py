import os
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

    def resume_jd_match(self, resume_info=None, job_info=None):
        prompt_chat = PromptTemplate.from_template(
            """
            ### RESUME INFORMATION (OPTIONAL):
            {resume_info}

            ### JOB INFORMATION (OPTIONAL):
            {job_info}

            ### INSTRUCTION:
            Assume you are a Resume and JD match percentage expert for the candidate,
            Give percentage of match between the resume and the JD from 0 to 100%,
            by formula (count of common skills/ total number of skills in JD ),
            also tell which skills match and which dont in resume but requires in JD, 
            If all common skills match then give 100% match score.
            Provide an intelligent and helpful response to the user’s query. 
            Tailor the response based on resume and job info are provided.
            ### RESPONSE:
            """
        )
        chain_chat = prompt_chat | self.llm
        res = chain_chat.invoke({
            "resume_info": resume_info or "No resume info provided.",
            "job_info": job_info or "No job info provided."
        })
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
