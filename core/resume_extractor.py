import re
from ast import Raise
from collections import defaultdict
from typing import Dict, List

import spacy
from pathy import ABC
from spacy import displacy
from spacy.matcher import Matcher
from spacy.util import filter_spans


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
        self.nlp = spacy.blank('en')
        self.ruler = self.nlp.add_pipe(
            'entity_ruler', config={
                'validate': True
            }).from_disk('ruler/heading_pattern.jsonl')

    def fit(self, text: str):
        """Fit model to content, call to_dict() to get heading group values

        Args:
            text (str): resume content as text
        """
        self.doc = self.nlp(text)

    def get_dict(self) -> Dict[str, str]:
        """Extract readed resume content to dictionary
        """
        data = defaultdict(str)

        last_key = "BASIC"
        last_key_link = ""

        for token in self.doc:
            if token.ent_type_ == "":
                data[last_key] += token.text_with_ws
                if last_key_link:
                    data[last_key_link] += token.text_with_ws
                continue

            if token.ent_type_ != last_key:
                if last_key == "WORK_EXPERIENCE":
                    if token.ent_type_ == "SKILLS":
                        continue

                    if token.ent_type_ == "PROJECT":
                        last_key_link = last_key
                    else:
                        last_key_link = ""

                last_key = token.ent_type_

        return data

    def get_html(self):
        return displacy.render(self.doc, style="ent")


class SpanExtractor(Extractor):
    def __init__(self):
        import srsly
        patterns = srsly.read_jsonl("ruler/skill_patterns.jsonl")
        self.model = spacy.load("model/content_span")
        self.ruler = self.model.add_pipe(
            "span_ruler", before='spancat').add_patterns(patterns)
        self.available_labels = self.model.get_pipe("spancat").labels

    def fit(self, text: str):
        self.doc = self.model(text)
        return self.doc

    def get_dict(self) -> Dict[str, str]:
        data = defaultdict(list)

        for span in self.doc.spans["sc"]:
            data[span.label_] += [span]

        return data

    def get_html(self):
        return displacy.render(self.doc, style="span")


class ContentExtractor(Extractor):
    def __init__(self):
        import srsly
        self.model = spacy.load("model/content_ner_v1")
        self.ruler = self.model.add_pipe(
            'entity_ruler',
            name="ruler1",
            config={
                'validate': True
            },
            after='ner').from_disk('ruler/skill_patterns.jsonl')
        self.ruler1 = self.model.add_pipe(
            'entity_ruler',
            name="ruler2",
            config={
                'validate': True
            },
            before='ner').from_disk('ruler/basic_info_patterns.jsonl')
        self.available_labels = self.model.get_pipe("ner").labels

    def fit(self, text: str):
        self.doc = self.model(text)
        if not self.doc:
            return
        self.text = text
        phone_span = self.extract_phone(text)
        if phone_span:
            start_idx, end_idx = phone_span.span()
            span = self.doc.char_span(start_idx, end_idx, label="PHONE")
            ent_list = list(self.doc.ents)
            ent_list.append(span)
            if span:
                try:
                    self.doc.set_ents(list(ent_list))
                except Exception as e:
                    print(e.__traceback__)
                    print(str(e))

        return self.doc

    def extract_phone(self, text: str) -> List[str]:
        #phone_token = r"[(\+?84)0]\d{9,12}\s+"
        phone_token = r"[(\+?\d)0]{1,2}\s*\d{3}\s*\d{3}\s*\d{3}\b"
        return re.search(phone_token, text)

    def get_ents(self) -> List[List[str]]:
        data = []
        for ent in self.doc.ents:
            text = ent.text
            if ent.label_ == 'DATE':
                if text == '-':
                    continue
                text = text.lower()
                text = re.sub(
                    r"[^(january|february|march|april|may|june|july|august|september|october|november|december|now|present)\d+-\\/]",
                    "", text)
            data.append([ent.label_, text])
        return data

    def get_doc(self):
        return self.doc

    def get_dict(self) -> Dict[str, str]:
        data = defaultdict(list)

        for ent in self.doc.ents:
            data[ent.label_] += [ent]
        return data

    def get_html(self):
        return displacy.render(self.doc, style="ent")