import os
import re
from ast import Raise
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import langid
import spacy
from file_reader import pdf_checker, pdf_reader
from pathy import ABC
from preprocessor import preprocessor
from pyvi import ViTokenizer
from spacy import displacy
from spacy.matcher import Matcher
from spacy.util import filter_spans

DIR_PATH = os.path.dirname(__file__)


class Extractor(ABC):
    def fit(self, text: str):
        """Fit model to content, call to_dict() to get values

        Args:
            text (str): resumse content as text

        Returns: None
        """
        raise Exception("function not yet implements")

    def get_dict(self):
        """Get extracted values to a dictionary

        Returns: None
        """
        raise Exception("function not yet implements")

    def get_html(self):
        """Color entities, export to html format

        Returns: None
        """
        raise Exception("function not yet implements")


class HeadingExtractor(Extractor):
    def __init__(self):
        """
        The function initializes the spacy model, the pdf reader and the pdf checker. It also adds the
        entity ruler to the spacy model
        """
        self.nlp = spacy.blank("en")
        self.pdf_reader = pdf_reader.PDFReader()
        self.pdf_checker = pdf_checker.PDFChecker()
        self.ruler = self.nlp.add_pipe(
            "entity_ruler", config={"validate": True}
        ).from_disk(f"{DIR_PATH}/ruler/heading_pattern.jsonl")

    def fit(self, file_):
        """
        It reads the pdf file, checks if it's a readable pdf or not, if it's not, it reads it again with
        another engine

        :param file_: file object
        :return: The doc object is being returned.
        """

        cv_content = self.pdf_reader.read(file_, fast=True)
        self.doc = self.nlp(cv_content)

        if self.pdf_checker.detect(cv_content, self.get_dict()):
            print("Reading pdf again with another engine")
            cv_content = self.pdf_reader.read(file_, fast=False)
            self.doc = self.nlp(cv_content)

        self.cv_content = cv_content
        self.lang = self.language_dectect()
        return self.doc

    def fit_str(self, text):
        self.doc = self.nlp(text)
        self.lang = self.language_dectect()
        return self.doc

    def language_dectect(self):
        en, vi = 0, 0
        for k, v in self.get_dict().items():
            if langid.classify(v)[0] == "en":
                en += 1
            else:
                vi += 1
        return "en" if en > vi else "vi"

    def get_dict(self) -> Dict[str, str]:
        """
        It takes a resume, and returns a dictionary of heading of the resume's content
        :return: A dictionary of the heading of resume content.
        """

        data = defaultdict(str)

        last_key = "BASIC"
        last_key_link = ""
        last_key_link_2 = ""

        for token in self.doc:
            if token.ent_type_ == "":
                data[last_key] += token.text_with_ws
                if last_key_link:
                    data[last_key_link] += token.text_with_ws
                if last_key_link_2:
                    data[last_key_link_2] += token.text_with_ws
                continue

            if token.ent_type_ != last_key:
                if last_key == "WORK_EXPERIENCE":
                    if token.ent_type_ == "SKILLS":
                        last_key_link_2 = "SKILLS"
                        continue
                    else:
                        last_key_link_2 = ""

                    if token.ent_type_ == "PROJECT":
                        last_key_link = last_key
                    else:
                        last_key_link = ""

                last_key = token.ent_type_

        return data

    def get_html(self):
        return displacy.render(self.doc, style="ent")


class ContentExtractor(Extractor):
    def __init__(self, lang="en"):
        """
        The function takes in a language parameter, and if the language is Vietnamese, it loads the
        Vietnamese model, and if the language is English, it loads the English model.

        If the language is neither Vietnamese nor English, it raises an error.

        The function also loads the entity ruler patterns from the ruler folder.

        The entity ruler patterns are the patterns that the model will use to extract entities.

        The function also gets the available labels of the model.

        The available labels are the labels that the model can extract.

        :param lang: language of the text to be processed, defaults to en (optional)
        """
        if lang == "vi":
            self.model = spacy.load(f"{os.path.dirname(DIR_PATH)}/model/vi_content_ner")
        elif lang == "en":
            self.model = spacy.load(f"{os.path.dirname(DIR_PATH)}/model/en_content_ner")
        else:
            raise ValueError("Invalid language")

        self.lang = lang

        self.ruler = self.model.add_pipe(
            "entity_ruler", name="ruler1", config={"validate": True}, after="ner"
        ).from_disk(f"{DIR_PATH}/ruler/skill_patterns.jsonl")
        self.ruler1 = self.model.add_pipe(
            "entity_ruler", name="ruler2", config={"validate": True}, before="ner"
        ).from_disk(f"{DIR_PATH}/ruler/basic_info_patterns.jsonl")
        self.available_labels = self.model.get_pipe("ner").labels

    def fit(self, text: str):
        """
        1. Tokenize the text if cv content is vietnamese else it remove accent from text
        2. Create a doc object using the model
        3. Extract the phone number from the text
        4. Create a span object for the phone number
        5. Add the span object to the list of entities
        6. Set the entities of the doc object to the list of entities

        :param text: The text to be processed
        :type text: str
        :return: The doc object
        """
        if self.lang == "vi":
            text = ViTokenizer.tokenize(text)
        else:
            text = preprocessor.remove_accents(text)

        self.doc = self.model(text)
        if not self.doc:
            return

        phone_span = self.extract_phone(text)
        ent_list = list(self.doc.ents)

        if phone_span:
            start_idx, end_idx = phone_span.span()
            span_phone = self.doc.char_span(
                start_idx, end_idx, label="PHONE", alignment_mode="contract"
            )
            ent_list.append(span_phone)
        print(ent_list)

        try:
            self.doc.set_ents(ent_list)
        except Exception as e:
            print(str(e))

        return self.doc

    def extract_phone(self, text: str):
        # phone_token = r"[(\+?84)0]\d{9,12}\s+"
        phone_token = (
            r"(\(?\+?\d{2,2}\)?|0)[\s\-\.]*\d{3}[\s\-\.]*\d{3}[\s\-\.]*\d{3}\b"
        )
        return re.search(phone_token, text)

    def extract_email(self, text: str):
        email_token = r"[\w.+-]+@[\w-]+\.[\w.-]+"
        return re.search(email_token, text)

    def get_ents(self) -> List[List[str]]:
        """
        1. Iterate through the tokens in the doc
        2. If the token is an entity, check if it's the beginning of a new entity (iob_ == "B")
        3. If it is, check if the previous entity was a "DOING" entity. If it was, add the previous entity
        to the current one.
        4. If it wasn't, add the previous entity to the list of entities.
        5. If the token is not an entity, add it to the current entity.
        6. If the token is the last token in the doc, add the current entity to the list of entities.
        :return: A list of lists, where each list contains the entity type and the entity text.
        """
        ents = []
        string_cat = ""
        string_not_cat = ""
        label = ""
        for token in self.doc:
            if token.ent_type:
                if token.ent_iob_ == "B":
                    if token.ent_type_ == "SKILL" and label == "DOING":
                        string_cat += token.text_with_ws + " "
                        continue
                    if label == "DOING":
                        string_cat += string_not_cat
                    elif len(string_not_cat.strip()) > 1:
                        ents.append(
                            [
                                "none",
                                string_not_cat.strip()
                                if self.lang == "en"
                                else string_not_cat.strip().replace("_", " "),
                            ]
                        )
                    if len(string_cat) > 1 and label:
                        ents.append(
                            [
                                label,
                                string_cat.strip()
                                if self.lang == "en"
                                else string_cat.strip().replace("_", " "),
                            ]
                        )
                    string_cat = ""
                    string_not_cat = ""
                    label = token.ent_type_

                if not preprocessor.is_special_char(token.text) and (
                    len(token.text) > 1 or token.is_alpha
                ):
                    string_cat += token.text_with_ws + " "
            else:
                if not preprocessor.is_special_char(token.text) and (
                    len(token.text) > 1 or token.is_alpha
                ):
                    string_not_cat += token.text_with_ws + " "

        if label == "DOING":
            string_cat += string_not_cat
        elif len(string_not_cat.strip()) > 1:

            ents.append(
                [
                    "none",
                    string_not_cat.strip()
                    if self.lang != "vi"
                    else string_not_cat.strip().replace("_", " "),
                ]
            )
        if len(string_cat) > 1 and label:
            ents.append(
                [
                    label,
                    string_cat.strip()
                    if self.lang != "vi"
                    else string_cat.strip().replace("_", " "),
                ]
            )

        return ents

    def get_doc(self):
        return self.doc

    def get_dict(self) -> Dict[str, str]:
        data = defaultdict(list)

        for ent in self.doc.ents:
            data[ent.label_] += [ent]
        return data

    def get_html(self):
        return displacy.render(self.doc, style="ent")
