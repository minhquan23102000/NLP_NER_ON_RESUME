import json
import os
import random
import re
from sre_parse import WHITESPACE
from tkinter.filedialog import test

import spacy
from pyvi import ViUtils
from sklearn.model_selection import train_test_split

PREPROCESS_CLASSES = [
    "PERSON_NAME", "ADDRESS", "EDUCATION", "GPA", "SKILL", "EXPERIENCE_LEVEL",
    "JOB_TITLE", "DATE_BIRTH", "MAJOR", "MARIAGE_STATUS", 'GENDER',
    'ORGANIZATION', 'LOCATION'
]

CORPUS_PATH = 'data/resume_annotations'
SAVE_PATH = 'data/spacy_ner_resume_corpus'

#Token to check if their are blank text (span) in corpus
WHITESPACE_TOKEN = re.compile('\s+')

#Get list corpus name
list_corpus_files = os.listdir(CORPUS_PATH)

#Train test spilt
train_corpus_files, val_corpus_files = train_test_split(list_corpus_files,
                                                        test_size=0.20,
                                                        random_state=0)
print("Shuffle list corpus done")

#Read data, convert corpus dtype from json spacy format to spacy training format
docBin = spacy.tokens.DocBin()
nlp = spacy.blank('en')

print("Start loading and converting corpus set")
#Train corpus
for file_name in train_corpus_files:
    file_path = f"{CORPUS_PATH}/{file_name}"

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        if len(data['annotations']) == 0:
            continue

        annotations = data['annotations'][0]

        text = annotations[0]
        doc = nlp(text)

        entities = annotations[1]['entities']
        ents_list = []
        for start_idx, end_idx, label in entities:
            span = doc.char_span(start_idx,
                                 end_idx,
                                 label=label,
                                 alignment_mode='contract')

            #Skip blank span
            if WHITESPACE_TOKEN.match(str(span).strip()) or len(
                    str(span)) == 0:
                print("skip")
                continue

            if span and label in PREPROCESS_CLASSES:
                ents_list.append(span)

        ent_list = spacy.util.filter_spans(ents_list)
        doc.ents = ents_list

    docBin.add(doc)

#Create saving folder
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

#Save train docBin
docBin.to_disk(f'{SAVE_PATH}/train.spacy')
print(
    f"Loading and converting training set done. Save at {SAVE_PATH}/train.spacy"
)

#Test corpus
docBin = spacy.tokens.DocBin()
for file_name in val_corpus_files:
    file_path = f"{CORPUS_PATH}/{file_name}"

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        if len(data['annotations']) == 0:
            continue

        annotations = data['annotations'][0]

        text = annotations[0]
        doc = nlp(text)

        entities = annotations[1]['entities']
        ents_list = []
        for start_idx, end_idx, label in entities:
            span = doc.char_span(start_idx,
                                 end_idx,
                                 label=label,
                                 alignment_mode='contract')

            #Skip blank span
            if WHITESPACE_TOKEN.match(str(span).strip()) or len(
                    str(span)) == 0:
                print("skip")
                continue

            if span and label in PREPROCESS_CLASSES:
                ents_list.append(span)

        ent_list = spacy.util.filter_spans(ents_list)
        doc.ents = ents_list

    docBin.add(doc)

#Save test set
docBin.to_disk(f'{SAVE_PATH}/val.spacy')
print(
    f"Loading and converting training set done. Save at {SAVE_PATH}/val.spacy")
