import glob
import os
import random
import re
import shutil

import langid
import tqdm
from file_reader.pdf_reader import PDFReader

pdf_reader = PDFReader()
save_path = '.'
corpus_path = list(glob.glob('..\\..\\CV_Parse\\resource\\CV\\IT\\**\\*.pdf'))
corpus_path += list(glob.glob('..\\..\\CV_Parse\\resource\\CV\\CV2\\*.pdf'))
random.shuffle(corpus_path)

if not os.path.exists(save_path):
    os.makedirs(save_path)

id = 0
for path in tqdm.tqdm(corpus_path, "Sorting cv", unit='files'):
    with open(path, 'rb') as f:
        cv_content = pdf_reader.read(f, fast=True)
        filename = path.replace(".pdf", "").split('\\')[-1]
        #print(langid.classify(cv_content))

        if langid.classify(cv_content)[0] == 'en':
            shutil.copyfile(path, f"{save_path}/eng/{filename}_{id}.pdf")
        else:
            shutil.copyfile(path, f"{save_path}/vi/{filename}_{id}.pdf")

    id += 1
