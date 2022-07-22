import glob
import json
import os
import re
import sys
from typing import Iterable

import spacy

from core.resume_extractor import HeadingExtractor
from file_reader.pdf_reader import PDFReader

DATA_PATH = '../cv_data/data'

JSON_PATH = f"{DATA_PATH}/json"
PDF_PATH = f"{DATA_PATH}/pdf"
nlp = spacy.blank('vi')

def create_label_span(label, text):
    return {"label": label, "text": text}

def clean_ent(ent):
    ent = re.sub(r'(\s\|\s)', '|', ent)
    ent = re.sub(r'^\s*\.*-*|\s*\.*-*$', '', ent)
    ent = re.sub(r'^\s*\.*-*|\s*\.*-*$', '', ent)
    ent = re.sub(r'^\s*\.*-*|\s*\.*-*$', '', ent)

    ent = re.sub(r'[\(\)\[\]\{\}]', '\(\1', ent)
    return ent

def create_ents(doc, spans:Iterable, label:str):
    ents = []
    for span in spans:
        #print(span)
        span = span.span()
        span = doc.char_span(span[0], span[1], label=label, alignment_mode='contract')
        if span:
            ents.append(span)
    return ents

def create_doc(content, *args):
    doc = nlp(content)
    ents = []
    for ent in args:
        if not ent.get('text', ""):
            continue
        #print(ent['text'])
        spans = re.finditer(clean_ent(ent['text']), doc.text)
        ents += create_ents(doc, spans, ent['label'])
    if ents:
        ents = spacy.util.filter_spans(ents)
        print(ents)
        doc.set_ents(ents)

    return doc

def create_basic_doc(content:str, basics_json):
    person_name = basics_json.get('name', "")
    job_title = basics_json.get("label", "")
    address = basics_json.get("location", "")
    if address: address = address.get('address', "")
    date_birth = basics_json.get('dateBirth', "")

    args = []
    args.append(create_label_span("PERSON_NAME", person_name))
    args.append(create_label_span("JOB_TITLE", job_title))
    args.append(create_label_span("ADDRESS", address))
    args.append(create_label_span("DATE_BIRTH", date_birth))

    return create_doc(content, *args)

def create_education_doc(content:str, data):
    args = []
    for education in data:
        institution = education.get('institution', "")
        area = education.get('area', "")
        studyType = education.get('studyType', "")
        startDate = education.get('startDate', "")
        endDate = education.get('endDate', "")
        score = education.get('score', "")

        args.append(create_label_span("ORG", institution))
        args.append(create_label_span("MAJOR", area))
        #args.append(create_label_span("EDUCATION_LEVEL", studyType))
        args.append(create_label_span("DATE", startDate))
        args.append(create_label_span("DATE", endDate))
        args.append(create_label_span("GPA", score))

    return create_doc(content, *args)

def create_skill_doc(content:str, data):
    args = []
    hard_skills = []
    soft_skills = []
    for skill in data:
        if skill.get('name')== 'Hard Skill':
            hard_skills += skill.get('keywords', [])
        else:
            soft_skills += skill.get('keywords',[])

    for skill in hard_skills:
        args.append(create_label_span("HARD_SKILL", skill))
    for skill in soft_skills:
        args.append(create_label_span("SOFT_SKILL", skill))

    return create_doc(content, *args)

def create_work_doc(content:str, data):
    args = []
    for work in data:
        name = work.get('name',"")
        position = work.get('position',"")
        startDate = work.get('startDate', "")
        endDate = work.get('endDate', "")
        highlights = work.get('highlights', [])
        doing = []
        for h in highlights:
            h = re.split(r'[\n\.]+', h)
            doing.extend(h)

        args.append(create_label_span("ORG", name))
        args.append(create_label_span("JOB_TITLE", position))
        args.append(create_label_span("DATE", startDate))
        args.append(create_label_span("DATE", endDate))

        for do in doing:
            if do:
                args.append(create_label_span("DOING", do))

    return create_doc(content, *args)

def create_project_doc(content:str, data):
    args = []
    for project in data:
        name = project.get('name', "")
        roles = project.get('roles', [])
        startDate = project.get('startDate', "")
        endDate = project.get('endDate', "")
        highlights = project.get('highlights', [])
        keywords = project.get('keywords', [])

        doing = []
        for h in highlights:
            h = re.split(r'[\n\.]+', h)
            doing.extend(h)

        args.append(create_label_span("PROJECT_NAME", name))
        args.append(create_label_span("DATE", startDate))
        args.append(create_label_span("DATE", endDate))
        args.extend([create_label_span("JOB_TITLE", role) for role in roles])
        args.extend([create_label_span("HARD_SKILL", skill) for skill in keywords])

        for do in doing:
            if do:
                args.append(create_label_span("DOING", do))


    return create_doc(content, *args)

def create_hobby_doc(content:str, data):
    args = []
    for hobbies in data:
        hob = hobbies.get('keywords', [])
        args.extend([create_label_span("HOBBY", h) for h in hob])

    return create_doc(content, *args)


if __name__ == '__main__':
    pdf_reader = PDFReader()
    heading_extractor = HeadingExtractor()
    docBin = spacy.tokens.DocBin()
    for path in glob.glob(f"{PDF_PATH}/*.pdf")[7:15]:
        with open(path, 'rb') as f:
            cv_content = pdf_reader.read(f)
            heading_extractor.fit(cv_content)
            heading_content = heading_extractor.get_dict()


        filename = path.split('\\')[-1]
        filename = filename.replace('.pdf', '.json')
        with open(f'{JSON_PATH}/{filename}', 'r', encoding='utf-8') as f:
            json_resume = json.loads(f.read())

        basic_doc = create_basic_doc(heading_content['BASIC'], json_resume.get('basics', {}))
        education_doc = create_education_doc(heading_content['EDUCATION'], json_resume.get('education',[]))
        skill_doc = create_skill_doc(heading_content['SKILLS'], json_resume.get('skills', []))
        work_doc = create_work_doc(heading_content['WORK_EXPERIENCE'], json_resume.get('work', []))
        project_doc = create_project_doc(heading_content['PROJECT'], json_resume.get('projects', []))
        hobby_doc = create_hobby_doc(heading_content['HOBBIES'], json_resume.get('interests', []))

        docBin.add(basic_doc)
        docBin.add(education_doc)
        docBin.add(skill_doc)
        docBin.add(work_doc)
        docBin.add(project_doc)
        docBin.add(hobby_doc)









