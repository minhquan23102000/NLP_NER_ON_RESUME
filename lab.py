import re

from core.resume_extractor import ContentExtractor

test_string = """
05/2022 NOW \nINTERN DATA SCIENTIST NLP, FPT INFORMATION SYSTEM \n \nCollect and labeling CVs dataset for trainning NER model, help the company have a \nvaluable data on develop marchine model for resumes handling bussiness. \n \nBuild a bot that can read resumes by applying NER and transformers. Help HR \nappartment, automatively filtering resumes, reduces the overall cost in 30%. \n09/2021 05/2022 \nAI STUDENT RESEARCHER, HUTECH UNIVERSITY \n \nAnalysis bussiness in handling the operation of administrative papers. Help the team \nunderstand deeply the bussiness before continue to build model. \n \nBuilding Chatbot for automative guide people doing paperworks, reduce the average \nwaiting time by 80%, while ensuring the continuation and enhancements of services. \n \nDevelop OCR to read data from images such as ID cards, household papers, help people \neasily doing paper works. \n \nJoin final round of Hutech Startup Wings as an AI startup product and won most \nimpression project prize. \n04/2020 07/2021 \nDATA SCIENTIST STUDENT, VNUHCM UNIVERSITY \n \nHand on prediction models such as (price regression, text classification using Decisson \nTree, KNN, Random forests, SVM, Navie Bayes, XGBoost... \n \nHand on recommendation system and big data preprocessing using PySpark library \n\n2 \n \ntime series analysis (Fbprophet, SARIMA) and RFM customer \nsegmentation using clustering algorithms such as (Kmean, GMM, DBScan) \n \n
"""

nlp = ContentExtractor()

doc = nlp.fit(test_string)


for ent in nlp.get_ents():
    print(ent[0], ent[1])
