import re
from collections import defaultdict
from typing import Dict, List, Set

import fitz
import pdfplumber
import spacy
from dateutil import parser
from spacy import displacy
from urlextract import URLExtract

import text_preprocessing

NER_LABEL = {
    "PERSON_NAME": "rgb(238,179,252, 1);",
    "ADDRESS": "rgb(238,174,202);",
    "EDUCATION": "#FFF5EE",
    "GPA": "#F9F1F0;",
    "SKILL": "#EF9",
    "EXPERIENCE_LEVEL": "#F8AFA6",
    "JOB_TITLE": "#FAEBD7",
    "DATE_BIRTH": "#FFDEAD",
    "MAJOR": "#FFC0CB",
    "MARIAGE_STATUS": "#FFF0F5",
    "ORGANIZATION": "#E0FFFF",
    "GENDER": "#E0FFAA",
    "LOCATION": "#FFAAFF",
}


class ResumeExtractor(object):
    def __init__(self, ner_model_path: str):
        self.nlp = spacy.load(ner_model_path)

    def extract_text_from_pdf_file(self, file):
        cv_content = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                cv_content += page.extract_text() + " "

        cv_content = text_preprocessing.clean_text(cv_content)
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

        cv_text = text_preprocessing.clean_text(cv_text)

        return cv_text

    def extract_email(self, text: str) -> List[str]:
        email_token = r"[\w.+-]+@[\w-]+\.[\w.-]+"
        return re.findall(email_token, text)

    def extract_url(self, text: str) -> List[str]:
        extractor = URLExtract()
        return extractor.find_urls(text)

    def extract_phone(self, text: str) -> List[str]:
        #phone_token = r"[(\+?84)0]\d{9,12}\s+"
        phone_token = r"[(\+?\d)0]{1,2}\s*\d{3}\s*\d{3}\s*\d{3}\b"
        return re.findall(phone_token, text)

    def format_date(self, date_str):
        try:
            date = parser.parse(date_str)
            date_format = f"{date.day}-{date.month}-{date.year}"
        except Exception as e:
            print(str(e), e.__cause__)
            date_format = date_str

        return date_format

    def get_summary(self, resume_path: str) -> Dict[str, Set[str]]:
        dic = defaultdict(set)
        resume_content = self.extract_text_from_pdf(resume_path)
        doc = self.nlp(resume_content)

        for token in doc.ents:
            if token.label_ == "DATE_BIRTH":
                dic[token.label_].add(self.format_date(token.text))
            else:
                dic[token.label_].add(token.text)

        dic["EMAIL"] = set(self.extract_email(resume_content))
        dic["PROFILE_URL"] = set(self.extract_url(resume_content))
        dic["PHONE"] = set(self.extract_phone(resume_content))

        return dic

    def get_summary_from_text(self, resume_content: str) -> Dict[str, Set[str]]:
        dic = defaultdict(set)
        doc = self.nlp(resume_content)

        for token in doc.ents:
            if token.label_ == "DATE_BIRTH":
                dic[token.label_].add(self.format_date(token.text))
            else:
                dic[token.label_].add(token.text)

        dic["EMAIL"] = set(self.extract_email(resume_content))
        dic["PROFILE_URL"] = set(self.extract_url(resume_content))
        dic["PHONE"] = set(self.extract_phone(resume_content))

        for key, values in dic.items():
            dic[key] = list(values)

        return dic

    def render_html_entities(self, resume_content: str):
        doc = self.nlp(resume_content)
        options = {'colors': NER_LABEL}
        return displacy.render(doc, 'ent', page=True, options=options)
