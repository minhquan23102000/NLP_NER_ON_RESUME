import docx
import fitz
import pdfplumber
from streamlit.uploaded_file_manager import UploadedFile

import text_preprocessing


class ResumeReader(object):
    def __init__(self, need_clean=True):
        self.need_clean = need_clean
        pass

    def extract_text_from_pdf_file(self, file):
        cv_content = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                cv_content += page.extract_text() + " "

        return cv_content

    def extract_text_from_pdf(self, filename):
        """Extract raw text content from pdf file

        Args:
            filename (_type_): _description_
        """
        pdf = fitz.open(filename)
        cv_text = ""
        for page in pdf:
            cv_text += page.get_text() + " "

        return cv_text

    def extract_text_from_doc(self, file):
        document = docx.Document(file)

        text = ''
        for p in document.paragraphs:
            text += ' ' + p.text

        return text


    def read_text_from_file(self, resume_file: UploadedFile):
        text = ''
        mime_type = resume_file.name.split('.')[-1]
        if mime_type == 'pdf':
            text = self.extract_text_from_pdf_file(resume_file)
        elif mime_type == 'docx':
            text = self.extract_text_from_doc(resume_file)

        if self.need_clean:
            text = text_preprocessing.clean_text(text)

        return text
