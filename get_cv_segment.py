import glob
import os
import random
import re

import tqdm

import resume_parser.resume_extractor as resume_extractor
from file_reader.pdf_reader import PDFReader

heading_extractor = resume_extractor.HeadingExtractor()
pdf_reader = PDFReader()
save_path = 'D:\Study_Zone\Data_Science\DS_Project\CV_Parse\data/cv_segment_text'
corpus_path = random.choices(glob.glob('..\\CV_Parse\\resource\\CV\\IT\\**\\*.pdf'), k=12)
random.shuffle(corpus_path)

if not os.path.exists(save_path):
    os.makedirs(save_path)

for path in tqdm.tqdm(corpus_path, "Segmenting Resume", unit='files'):
    with open(path, 'rb') as f:
        cv_content = pdf_reader.read(f, fast = True)
        heading_extractor.fit(cv_content)
        heading = heading_extractor.get_dict()
        filename = path.replace(".pdf", "").split('\\')[-1]
        for k, v in heading.items():
            if v:
                with open(f"{save_path}/{filename}_{k}.txt", 'w') as w:
                    w.write(v)



