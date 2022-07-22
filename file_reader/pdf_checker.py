class PDFChecker(object):
    def __init__(self):
        self.basic_threshold = 0.048882
        self.work_threshold = 0.238021
        self.project_threshold = 0.000398
        self.education_threshold = 0.026845
        self.skill_threshold = 0.002407
        self.momentum_threshold = 3

    def detect(self, resume_content:str, resume_heading:dict) -> bool:
        """return true if failed to read resume content

        Args:
            resume_content (str): _description_
            resume_heading (dict): _description_

        Returns:
            bool: _description_
        """
        cv_len = len(resume_content)

        if cv_len == 0: return True

        basic_ratio = len(resume_heading.get("BASIC", ""))/cv_len
        work_ratio = len(resume_heading.get("WORK_EXPERIENCE", ""))/cv_len
        project_ratio = len(resume_heading.get("PROJECT", ""))/cv_len
        education_ratio = len(resume_heading.get("EDUCATION", ""))/cv_len
        skill_ratio = len(resume_heading.get("SKILLS", ""))/cv_len


        momentum = 0

        momentum += basic_ratio < self.basic_threshold
        momentum += work_ratio < self.work_threshold
        momentum += project_ratio < self.project_threshold
        momentum += education_ratio < self.education_threshold
        momentum += skill_ratio < self.skill_threshold
        print("Momentum: ", momentum)

        return momentum >= self.momentum_threshold
