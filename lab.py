import re

from core.resume_extractor import ContentExtractor

test_string = """
09/2021 – 05/2022
AI STUDENT RESEARCHER, HUTECH UNIVERSITY
•	Analysis bussiness in handling the operation of administrative papers. Help the team understand deeply the bussiness before continue to build model.
•	Building Chatbot for automative guide people doing paperworks, reduce the average waiting time by 80%, while ensuring the continuation and enhancements of services.
•	Develop OCR to read data from images such as ID cards, household papers, help people easily doing paper works.
•	Join final round of Hutech Startup Wings as an AI startup product and won most impression project prize.
04/2020 – 07/2021
DATA SCIENTIST STUDENT, VNUHCM UNIVERSITY
•	Hand on prediction models such as (price regression, text classification...) using Decisson Tree, KNN, Random forests, SVM, Navie Bayes, XGBoost...
•	Hand on recommendation system and big data preprocessing using PySpark library
•	Experience with time series analysis (Fbprophet, SARIMA) and RFM customer segmentation using clustering algorithms such as (Kmean, GMM, DBScan)
"""

nlp = ContentExtractor()

doc = nlp.fit(test_string)


for ent in nlp.get_ents():
    print(ent[0], ent[1])
