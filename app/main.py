import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import json

from chains import Chain
from utils import extract_raw_text_from_pdf

def create_streamlit_app(llm):
    st.title("📄 Cover Letter Generator & Chat Assistant")

    col1, col2 = st.columns([1, 3])

    # Resume uploader (automatic processing on upload)
    with col1:
        uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"], key="resume_uploader")
        
        # Automatically process the resume once uploaded
        if uploaded_file is not None:
            resume_text = extract_raw_text_from_pdf(uploaded_file)
            resume_info = llm.extract_resume_details(resume_text)
            st.session_state["resume_uploaded"] = uploaded_file
            st.session_state["resume_info"] = resume_info
            st.success("Resume details extracted and saved!")

        # Job description link input
        url_input = st.text_input("Enter the Job URL:", value=st.session_state.get("job_url", "https://rocketlane.freshteam.com/jobs/hzabyJhRp-od/react-frontend-developer"), key="job_url_input")
        if url_input:
            st.session_state["job_url"] = url_input
        
        # Submit button for JD processing
        submit_button = st.button("Submit")

        # Job data extraction when submit button is pressed
        if submit_button:
            if "job_url" in st.session_state:
                try:
                    loader = WebBaseLoader([st.session_state["job_url"]])
                    job_data = loader.load().pop().page_content
                    jobs = llm.extract_jobs(job_data)
                    st.session_state["job_data"] = jobs
                    st.success("Job details extracted and saved!")
                except Exception as e:
                    st.error(f"An Error Occurred while extracting the job details: {e}")
            else:
                st.error("Please provide a Job URL.")

        # Quick Cover Letter Generator button (stays on the left)
        if st.button("Quick Cover Letter Generator"):
            st.session_state["generate_cover_letter"] = True

    # Chat and Cover Letter Generation section (on the right)
    with col2:
        # Chat section for interacting with LLM
        st.write("### Chat with LLM Assistant")

        # Chat input
        chat_input = st.text_input("Ask for resume improvements, job advice, or any other question:")
        
        # Chat functionality
        if st.button("Send"):
            try:
                resume_info = st.session_state.get("resume_info", None)
                jobs = st.session_state.get("job_data", None)
                if resume_info and jobs:
                    response = llm.chat_with_llm(chat_input, resume_info=resume_info, job_info=jobs[0])
                elif resume_info:
                    response = llm.chat_with_llm(chat_input, resume_info=resume_info)
                else:
                    response = llm.chat_with_llm(chat_input)
                
                st.write(f"### AI:\n {response}")
            except Exception as e:
                st.error(f"An error occurred while chatting: {e}")
        
        # Show the cover letter output in the right column if button clicked
        if st.session_state.get("generate_cover_letter", False):
            if "resume_info" in st.session_state and "job_data" in st.session_state:
                resume_info = st.session_state["resume_info"]
                jobs = st.session_state["job_data"]
                for job in jobs:
                    cover_letter = llm.write_cover_letter(job, resume_info)
                    st.markdown(f"### Cover Letter for {job['role']} at {job['company_name']}")
                    st.code(cover_letter, language='markdown')
            else:
                st.error("Both resume and job details are required for generating a cover letter.")
            st.session_state["generate_cover_letter"] = False  # Reset state after showing



if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cover Letter Generator & Assistant", page_icon="📄")
    create_streamlit_app(chain)