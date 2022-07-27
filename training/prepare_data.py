import glob
import json
import os
import re
import sys
from datetime import date
from functools import reduce
from typing import Iterable

import spacy

sys.path.insert(0, os.path.abspath(f'{os.path.dirname(os.path.dirname(__file__))}'))
import langid
from core.resume_extractor import HeadingExtractor
from file_reader.pdf_reader import PDFReader
from pyvi import ViTokenizer
from underthesea import sent_tokenize

DATA_PATH = '../../cv_data/data'

JSON_PATH = f"{DATA_PATH}/json"
PDF_PATH = f"{DATA_PATH}/pdf"

#Init model
nlp = spacy.blank('en')

total_token_counts = 0
invalid_token_counts = 0

def create_label_span(label, text):
    return {"label": label, "text": str(text)}

def strip_ent(ent):
    l = 0
    r = len(ent)-1
    while l <= r:
        if re.match(r'[^\w\d+#%]', ent[l]):
            l += 1
        else:
            break

    while r >= 0:
        if re.match(r'[^\w\d+#%]', ent[r]):
            r -= 1
        else:
            break

    return ent[l:r+1]

def get_date_span(text):
    nlp_t = spacy.load('en_core_web_sm')
    doc = nlp_t(text)

    for ent in doc.ents:
        if ent.label_ == 'DATE':
            break

    return ent.text

def clean_ent(ent):
    ent = re.sub(r'(\s\|\s)', '|', ent)
    ent = strip_ent(ent)
    ent = re.sub(r'[\(\)\[\]\{\}]', '\\\1', ent)
    ent = re.sub(r'[\.\+\*\\]', '\\\1', ent)
    return ent

def create_ents(doc, spans:Iterable, label:str, text=""):
    global total_token_counts, invalid_token_counts
    ents = []
    for span in spans:
        #print(span)
        span_idx = span.span()
        span = doc.char_span(span_idx[0], span_idx[1], label=label, alignment_mode='contract')
        total_token_counts += 1
        if span:
            ents.append(span)
        else:
            invalid_token_counts+=1
    return ents

def create_doc(content, *args):
    doc = nlp(content)
    ents = []
    for ent in args:
        if not ent.get('text', ""):
            continue
        #Skip eng corpus only take vi corpus
        if langid.classify(ent.get('text'))[0] == 'en' and ent['label'] in ['DOING']:
            continue
        clean_ent_ = clean_ent(ent['text'])
        spans = re.finditer(f"{clean_ent_}", doc.text)
        ents += create_ents(doc, spans, ent['label'], clean_ent_)
    if ents:
        ents = spacy.util.filter_spans(ents)
        doc.set_ents(ents)
        print(doc.ents)

    return doc

def create_basic_doc(content:str, basics_json):
    person_name = basics_json.get('name', "")
    job_title = basics_json.get("label", "")
    address = basics_json.get("location", "")
    if address: address = address.get('address', "")
    date_birth = basics_json.get('dateBirth', "")
    if date_birth:
        date_birth = get_date_span(content)

    args = []
    args.append(create_label_span("PERSON_NAME", person_name))
    args.append(create_label_span("JOB_TITLE", job_title))
    args.append(create_label_span("ADDRESS", address))
    args.append(create_label_span("DATE", date_birth))

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
        #args.append(create_label_span("GPA", score))

    return create_doc(content, *args)

def create_skill_doc(content:str, data):
    args = []
    hard_skills = []
    soft_skills = []
    for skill in data:
        if skill.get('name')== 'Hard skill':
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
            h = sent_tokenize(h)
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
            h = sent_tokenize(h)
            doing.extend(h)


        args.append(create_label_span("PROJECT_NAME", name))
        args.append(create_label_span("DATE", startDate))
        args.append(create_label_span("DATE", endDate))
        args.extend([create_label_span("JOB_TITLE", role) for role in roles])
        #args.extend([create_label_span("HARD_SKILL", skill) for skill in keywords])

        for do in doing:
            if do:
                args.append(create_label_span("DOING", do))


    return create_doc(content, *args)

def create_hobby_doc(content:str, data):
    args = []
    for hobbies in data:
        hob = hobbies.get('keywords', [])
        if hob:
            args.extend([create_label_span("HOBBY", h) for h in hob])

        hob_name = hobbies.get('name', "")
        if hob_name:
            args.append(create_label_span("HOBBY", hob_name))

    return create_doc(content, *args)

def create_certificate_doc(content:str, data):
    args = []
    for certificate in data:
        #print("Certificate: ",certificate)
        certificate_name = certificate.get('name', "")
        date = certificate.get('date', "")
        issuer = certificate.get('issuer', "")

        args.append(create_label_span("CERTIFICATE", certificate_name))
        args.append(create_label_span("DATE", date))
        args.append(create_label_span("ORG", issuer))
    #print(args)

    return create_doc(content, *args)


if __name__ == '__main__':
    heading_extractor = HeadingExtractor()
    docBin = spacy.tokens.DocBin()
    print("Start to convert data to spacy format")
    for path in glob.glob(f"{PDF_PATH}/*.pdf"):
        with open(path, 'rb') as f:
            heading_extractor.fit(f)
            heading_content = heading_extractor.get_dict()


        filename = path.split('\\')[-1]
        filename = filename.replace('.pdf', '.json')
        try:
            with open(f'{JSON_PATH}/{filename}', 'r', encoding='utf-8') as f:
                json_resume = json.loads(f.read())
        except FileNotFoundError as e:
            print(e)
            continue

        basic_doc = create_basic_doc(heading_content['BASIC'], json_resume.get('basics', {}))
        education_doc = create_education_doc(heading_content['EDUCATION'], json_resume.get('education',[]))
        #skill_doc = create_skill_doc(heading_content['SKILLS'], json_resume.get('skills', []))
        work_doc = create_work_doc(heading_content['WORK_EXPERIENCE'], json_resume.get('work', []))
        project_doc = create_project_doc(heading_content['PROJECT'], json_resume.get('projects', []))
        hobby_doc = create_hobby_doc(heading_content['HOBBIES'], json_resume.get('interests', []))
        certificate_doc = create_certificate_doc(heading_content['EDUCATION'], json_resume.get('certificates',[]))

        docBin.add(basic_doc)
        docBin.add(education_doc)
        #docBin.add(skill_doc)
        docBin.add(work_doc)
        docBin.add(project_doc)
        docBin.add(hobby_doc)
        docBin.add(certificate_doc)

    print("Done")
    print(f"Total tokens: {total_token_counts}. Total invalid tokens: {invalid_token_counts}")
    print(f"{invalid_token_counts/total_token_counts:.2f} invalid tokens in corpus")

    db = spacy.tokens.DocBin().from_disk('corpus/phoner_covid.spacy')
    docBin.merge(db)

    docBin.to_disk('train.spacy')









