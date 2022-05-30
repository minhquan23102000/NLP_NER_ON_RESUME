import streamlit as st
from spacy import displacy

from text_extractor import NER_LABEL, ResumeExtractor
from text_preprocessing import clean_text

extractor = ResumeExtractor(ner_model_path='resume_ner_model/model-best')
st.set_page_config(page_title="Resume summary extractor",
                   layout='wide')
st.header("Resume summary extractor with NER")

pdf_file = st.file_uploader("Choose your resume file", accept_multiple_files=False, type=['pdf', 'doc', 'docx'])

if pdf_file:
    resume_content = extractor.extract_text_from_pdf_file(pdf_file)

    #Get summary from resume
    resume_summary = extractor.get_summary_from_text(resume_content)
    st.write(resume_summary)

    #Render html entities on resume
    html = extractor.render_html_entities(resume_content)
    st.markdown(html, unsafe_allow_html=True)


