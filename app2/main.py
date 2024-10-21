import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from utils import extract_raw_text_from_pdf

def create_streamlit_app(llm):
    st.title("📄 AI Based Resume JD Matcher")

    # Resume uploader section
    st.subheader("Resume Input")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"], key="resume_uploader")

    if uploaded_file is not None and "resume_info" not in st.session_state:
        resume_text = extract_raw_text_from_pdf(uploaded_file)
        resume_info = llm.extract_resume_details(resume_text)
        st.session_state["resume_uploaded"] = uploaded_file
        st.session_state["resume_info"] = resume_info
        st.success("Resume details extracted and saved!")

    # Job description URL input section
    st.subheader("Job Description Input")
    url_input = st.text_input("Enter the Job URL:", value=st.session_state.get("job_url", "https://rocketlane.freshteam.com/jobs/hzabyJhRp-od/react-frontend-developer"), key="job_url_input")
    
    if url_input:
        st.session_state["job_url"] = url_input

    # Button to match resume and JD
    if st.button("Resume JD Match"):
        if "resume_info" in st.session_state and "job_url" in st.session_state:
            try:
                # Load the job description from the URL
                loader = WebBaseLoader([st.session_state["job_url"]])
                job_data = loader.load().pop().page_content
                job_info = llm.extract_jobs(job_data)

                # Match resume and JD
                resume_info = st.session_state["resume_info"]
                match_result = llm.resume_jd_match(resume_info, job_info)
                
                st.write(f"### Match Result:\n{match_result}")
            except Exception as e:
                st.error(f"An error occurred while processing: {e}")
        else:
            st.error("Please upload a resume and provide a job URL.")

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="centered", page_title="Resume JD Matcher", page_icon="📄")
    create_streamlit_app(chain)
