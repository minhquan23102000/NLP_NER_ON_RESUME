import json
import subprocess
from re import U

import streamlit as st

import resume_parser.resume_extractor as resume_extractor
from file_reader.pdf_reader import PDFReader
from resume_parser.resume_reader import ResumeReader
from ultils import buffer2base64

st.set_page_config(
    page_title="Read Your Resume", page_icon="img/app_icon.png", layout="wide"
)

st.markdown("### Welcome to Read your resume 👋")
st.markdown("""
    Import an resume and get your content json format!
    With this json format you can customize your resume automatically at jsonresume.org
""")


def reading_resume(resume):
    return resume_reader.read(resume)

with st.spinner("Loading model"):
    pdf2text = PDFReader()
    resume_reader = ResumeReader()

st.success("Model is ready to go")

cv_file = st.sidebar.file_uploader("Upload resume file", type=["pdf"])
cols = st.columns([1, 1])
if cv_file:

    # Read content resume
    cv_content = pdf2text.read(cv_file, fast=True)
    pdf_display = f'<embed src="data:application/pdf;base64,{buffer2base64(cv_file.getvalue())}" width=100% height="750" type="application/pdf">'
    cols[0].header("Your Resume")
    cols[0].markdown(pdf_display, unsafe_allow_html=True)

    # Extract resume with model
    st.markdown("### Json resume")
    info = reading_resume(cv_content)
    st.write(info)
    with open("resume.json", "w") as f:
        json.dump(info, f)

    resume_theme = st.sidebar.selectbox(
        "Choose a theme 👇", ["actual", "macchiato", "orbit", "monoblue"]
    )

    # Generate new resume
    resume_save_path = "resume.pdf"
    generate_resume_command = f"resume export {resume_save_path} --theme {resume_theme}"
    subprocess.run(generate_resume_command, shell=True)
    cols[1].header("New resume")
    with open(resume_save_path, "rb") as f:
        pdf_display_1 = f'<embed src="data:application/pdf;base64,{buffer2base64(f.read())}" width=100% height="750" type="application/pdf">'
        cols[1].markdown(pdf_display_1, unsafe_allow_html=True)


    # resume_reader.content_model.fit(cv_content)
    st.write(resume_reader.heading_model.get_dict())
    #st.write(cv_content)
    # st.write(resume_reader.content_model.get_dict())

    html = resume_reader.heading_model.get_html()
    st.markdown(html, unsafe_allow_html = True)
