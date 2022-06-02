import dill

from text_extractor import ResumeExtractor

extractor = ResumeExtractor('./resume_ner_model/model-best')

with open('ner_model.pkl','wb') as f:
    dill.dump(extractor, f)
