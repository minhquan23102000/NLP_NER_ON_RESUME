import re

from core.resume_extractor import ContentExtractor

test_string = """
NGUYE N MINH QUA N \nJUNIOR DATA SCIENTIST \nGo Vap, Ho Chi Minh 0383666401 minhquan23102000@gmail.com \nlinkedin.com/in/quan-minh/073265224/ github.com/minhquan23102000 \n
"""

nlp = ContentExtractor()

doc = nlp.fit(test_string)


for ent in nlp.get_ents():
    print(ent[0], ent[1])
