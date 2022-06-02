import streamlit as st

from file_reader import ResumeReader
from text_extractor import ResumeExtractor

st.set_page_config(page_title="Read Your Resume", page_icon = 'img/app_icon.png')
st.header("Let's Read Your Resume")

header_container = st.empty()

# Download model from cloud
if 'extractor' not in locals() and 'extractor' not in globals():
    with header_container.container():
        header_container.info('Starting to download model from cloud, please wait...')
        extractor = ResumeExtractor(ner_model_path='resume_ner_model/model-best')


#Ready to go
st.success("Model is ready to go!")
with header_container.container():
    header_container.header("Let's Read Your Resume")
resume_file = st.file_uploader("Choose your resume", accept_multiple_files=False, type=['pdf', 'docx'])
reader = ResumeReader()

if resume_file:
    with st.spinner("Reading resumes..."):
        resume_content = reader.read_text_from_file(resume_file)
        resume_summary = extractor.get_summary_from_text(resume_content)

    st.markdown("### Resume summary")
    st.write(resume_summary)

    #Render html entities on resume
    st.markdown("### Coloring resume")
    html = extractor.render_html_entities(resume_content)
    st.markdown(html, unsafe_allow_html=True)


