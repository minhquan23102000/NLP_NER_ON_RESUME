import random
from collections import defaultdict
from typing import Dict, List, Text

import spacy
from ultils import format_date, parse_url

from . import key_map_config
from .output_collector import Collector
from .resume_extractor import ContentExtractor, HeadingExtractor


class ResumeReader(object):
    def __init__(self):
        self.heading_model = HeadingExtractor()

    def read(self, resume_file) -> Dict[Text, Text]:
        """Read resume text content, then export to json format with schema like jsonresume.org

        Args:
            resume_file (file): resume content

        Returns:
            _type_: json
        """
        # self.resume_content = resume_content

        self.heading_model.fit(resume_file)
        if self.heading_model.lang == "en":
            self.content_model = ContentExtractor(lang="en")
        else:
            self.content_model = ContentExtractor(lang="vi")

        self.resume_content = self.heading_model.cv_content
        self.heading_segment_content = self.heading_model.get_dict()

        data = {}
        data["basics"] = self.get_basic_info()
        edu, cer = self.get_education()
        data["education"] = edu
        data["certificates"] = cer
        data["interests"] = self.get_hobbies()
        data["skills"] = self.get_skills()
        data["work"] = self.get_work_exp()
        data["projects"] = self.get_projects()
        data["references"] = self.get_reference()

        if not (data["basics"].get("name", None)):
            data["basics"].update(self.get_basic_info(self.resume_content))
            if not data["basics"].get("name", None):
                data["basics"]["name"] = "Unknown"

        # Correct date series
        self.correct_date_series(data["work"])
        self.correct_date_series(data["education"])
        self.correct_date_series(data["projects"])
        self.correct_date_series(data["certificates"])

        del self.heading_segment_content
        del self.resume_content
        return data

    def correct_date_series(self, container):
        for i, j in zip(range(0, len(container) - 1), range(1, len(container))):
            date_ = container[i].get("date", None)
            if date_:
                self.append_date(date_, container[j])

        return container

    def append_date(self, date, container):
        temp_date = container.get("startDate", None)
        temp_date_1 = container.get("endDate", None)
        container["startDate"] = date

        if temp_date is not None:
            container["endDate"] = temp_date

        if temp_date_1 is not None:
            container["date"] = temp_date_1

    def get_basic_info(self, text=None) -> Dict[Text, Text]:
        text = text if text else self.heading_segment_content["BASIC"]
        self.content_model.fit(text)
        data = defaultdict(list)
        data["profiles"] = []
        data["location"] = {"address": []}
        # print(self.content_model.get_ents())
        for key, value in self.content_model.get_ents():
            if key == "ADDRESS":
                data["location"]["address"].append(value)
            elif key == "URL":
                data["profiles"].append(parse_url(value))
            else:
                key = key_map_config.BASIC_MAP.get(key, "other")
                value = format_date(value) if key == "dateBirth" else value
                data[key].append(value)

        # Get summary text
        data["summary"] = (
            self.heading_segment_content["SUMMARY"]
            + "\n\n"
            + self.heading_segment_content["OBJECTIVE"]
        )
        # Compress data output
        for key, value in data.items():
            if key in ["profiles", "summary"]:
                continue
            if data[key] in ["email", "phone", "label"]:
                data[key] = " | ".join(value)
            elif key == "location":
                data["location"]["address"] = " | ".join(data["location"]["address"])
            else:
                try:
                    data[key] = min(value)
                except:
                    data[key] = value
        # Assign job title if is None
        if not data.get("label", None):
            data["label"] = data["other"]

        return data

    def get_education(self, text=None):
        self.content_model.fit(self.heading_segment_content["EDUCATION"])

        collect_points = {"institution", "area"}
        key_range = key_map_config.EDUCATION.keys()
        accepted_min_len = 3
        certificates = []

        class EducationCollector(Collector):
            def before_update_bundle(self, key, label, text):
                if key == "date":
                    if not self.bundle["startDate"]:
                        key = "startDate"
                    elif not self.bundle["endDate"]:
                        key = "endDate"
                elif label == "CERTIFICATE":
                    certificate = {
                        "name": text,
                        "date": self.bundle["startDate"],
                        "issuer": self.bundle["institution"],
                    }
                    certificates.append(certificate)
                    # self.reset_bundle()
                return key, text

        collector = EducationCollector(
            key_range, collect_points, accepted_min_len, key_map_config.EDUCATION_MAP
        )
        collector.collect(self.content_model.get_ents())

        return collector.get_container(except_key={"other"}), certificates

    def get_work_exp(self, text=None):
        self.content_model.fit(self.heading_segment_content["WORK_EXPERIENCE"])

        collect_points = {"name", "position"}
        key_range = set(key_map_config.WORK.keys())
        accepted_min_len = 2

        class WorkExpCollector(Collector):
            def before_update_bundle(self, key, label, text):
                if key == "date":
                    if not self.bundle["startDate"]:
                        key = "startDate"
                    elif not self.bundle["endDate"]:
                        key = "endDate"

                return key, text

        collector = WorkExpCollector(
            key_range, collect_points, accepted_min_len, key_map_config.WORK_MAP
        )
        collector.collect(self.content_model.get_ents())

        return collector.get_container(except_key={"highlights"})

    def get_projects(self, text=None):
        self.content_model.fit(self.heading_segment_content["PROJECT"])

        collect_points = {"name"}
        key_range = set(key_map_config.PROJECT.keys())
        accepted_min_len = 2

        class ProjectCollector(Collector):
            def before_update_bundle(self, key, label, text):
                if key == "date":
                    if not self.bundle["startDate"]:
                        key = "startDate"
                    elif not self.bundle["endDate"]:
                        key = "endDate"
                if key == "url":
                    text = text["url"]
                return key, text

        collector = ProjectCollector(
            key_range, collect_points, accepted_min_len, key_map_config.PROJECT_MAP
        )
        collector.collect(self.content_model.get_ents())

        return collector.get_container(except_key={"roles", "keywords", "highlights"})

    def get_hobbies(self, text=None):
        """Get hobbies content from input resume"""
        self.content_model.fit(self.heading_segment_content["HOBBIES"])
        data = []
        for label, text in self.content_model.get_ents():
            if label == "HOBBY":
                data.append({"name": text})

        return data

    def get_reference(self, text=None):
        self.content_model.fit(self.heading_segment_content["REFERENCE"])
        collect_points = {"name"}
        accepted_min_len = 3
        key_range = key_map_config.REFERENCE_MAP.values()

        reference_collector = Collector(
            key_range, collect_points, accepted_min_len, key_map_config.REFERENCE_MAP
        )
        reference_collector.collect(self.content_model.get_ents())

        container_data = reference_collector.get_container()

        # Concat email phone, job title into a big string, so it can be like requirement resume json structure
        for bundle in container_data:
            refer = ""
            for key, value in bundle.items():
                if value and key != "other":
                    refer += str(value) + ", "
            bundle["name"] = refer.rstrip(", ")
        return container_data

    def get_skills(self, text=None):
        """Get skills content from input resume"""
        text = text if text else self.heading_segment_content["SKILLS"]
        self.content_model.fit(text)
        hard_skills = []
        soft_skills = []
        for label, text in self.content_model.get_ents():
            if label == "SKILL" or label == "HARD_SKILL":
                hard_skills.append(text)
            else:
                soft_skills.append(text)

        if len(hard_skills) < 10:
            self.content_model.fit(self.resume_content)
            hard_skills = []
            for label, text in self.content_model.get_ents():
                if label == "SKILL":
                    hard_skills.append(text)

        return [
            {"name": "Key skills", "keywords": list(set(hard_skills))},
        ]

    def get_summary(self):
        return self.heading_segment_content["SUMMARY"]

    def to_pickle(self, output_path: str):
        import dill

        with open(output_path, "wb") as f:
            dill.dump(self, f, protocol=dill.HIGHEST_PROTOCOL)