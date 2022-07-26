import json
import os
import random
import shutil
import sys
from glob import glob

sys.path.append(os.path.abspath('../'))
from core.resume_reader import ResumeReader

CORPUS_PATH = '../../cv_data/eng'

DATA_PATH = '../../cv_data/data'

JSON_PATH = f"{DATA_PATH}/test_json"
PDF_PATH = f"{DATA_PATH}/test_pdf"


if __name__ == '__main__':
    model= ResumeReader()
    cv_paths = glob(f"{CORPUS_PATH}/*.pdf")

    random.shuffle(cv_paths)

    for path in cv_paths[:25]:
        with open(path, 'rb') as f:
            json_resume = model.read(f)

        filename = path.split('\\')[-1]
        json_name = filename.replace('.pdf', '.json')


        with open(f'{JSON_PATH}/{json_name}', 'w', encoding='utf-8') as f:
            json.dump(json_resume, f)

        shutil.copy(path, f'{PDF_PATH}/{filename}')



