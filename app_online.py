import json
import os
import pathlib
import subprocess
import sys

import dill
import requests
import streamlit as st
import streamlit.components.v1 as components

from core import resume_generator, resume_reader
from core.resume_reader import ResumeReader
from file_reader.pdf_reader import PDFReader
from ultils import buffer2base64

# sys.path.append("core/resume_reader.py")

st.set_page_config(page_title="Read Your Resume",
                   page_icon="img/app_icon.png",
                   layout="wide")

st.markdown("### Welcome to Read Your Resume 👋")
st.markdown("""
    Import an resume and get your resume content in json format!
    With this json you can ustomize your resume automatically at jsonresume.org.
    You can also use this json for filtering or scoring resumes.
""")

PATH = os.path.dirname(__file__)


def reading_resume(resume):
    return resume_reader.read(resume)


@st.cache(allow_output_mutation=True)
def load_model():
    import dill

    if os.name != "nt":
        pathlib.WindowsPath = pathlib.PosixPath

    with open(os.path.join(PATH, "core/resume_model.pkl"), "rb") as f:
        return dill.load(f)


notification = st.empty()
notification.info("Start downloading model, please wait...")
with st.spinner("Loading model"):
    pdf2text = PDFReader()
    resume_reader = load_model()

notification.success("Model is ready to go")

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

    # Save to json
    JSON_PATH = os.path.join(PATH, "resume.json")
    with open(JSON_PATH, "w") as f:
        json.dump(info, f)

    resume_theme = st.sidebar.selectbox(
        "Choose a theme 👇",
        ["eloquent-mod", "actual", "macchiato", "monoblue"])

    # Generate new resume
    resume_html = resume_generator.generate_resume(resume_theme)

    #Display resume on web
    cols[1].header("New resume")
    with cols[1]:
        components.html(resume_html, height=750, scrolling=True)

    # resume_reader.content_model.fit(cv_content)
    st.write(resume_reader.heading_model.get_dict())
    # st.write(resume_reader.content_model.get_dict())

    html = resume_reader.heading_model.get_html()
    st.markdown(html, unsafe_allow_html=True)
