BASIC_MAP = {
    "PERSON_NAME": "name",
    "JOB_TITLE": "label",
    "EMAIL": "email",
    "URL": "url",
    "SUMMARY": "summary",
    "PHONE": "phone",
    "DATE": "dateBirth",
    "MARIAGE_STATUS": "mariageStatus",
    "GENDER": "gender",
    "none": "none"
}

LOCATION_MAP = {"ADDRESS": "address"}


BASIC = {
    "name": "John Doe",
    "label": "Programmer",
    "image": "",
    "email": "john@gmail.com",
    "phone": "(912) 555-4321",
    "url": "https://johndoe.com",
    "summary": "A summary of John Doe…",
    "location": {
        "address": "2712 Broadway St",
    },
}

PROFILES = {"network": "Twitter", "username": "john", "url": "https://twitter.com/john"}

WORK = {
    "name": "Company",
    "position": "President",
    "startDate": "2013-01-01",
    "endDate": "2014-01-01",
    "highlights": [],
}

WORK_MAP = {
    "ORG": "name",
    "JOB_TITLE": "position",
    "DATE": "date",
    "DOING": "highlights",
    "SKILL": "keywords",
    "none": "unlabeled",
}

EDUCATION = {
    "institution": "University",
    "area": "Software Development",
    "studyType": "Bachelor",
    "startDate": "2011-01-01",
    "endDate": "2013-01-01",
    "score": "4.0",
}

EDUCATION_MAP = {
    "ORG": "institution",
    "MAJOR": "area",
    "EDUCATION_LEVEL": "studyType",
    "GPA": "score",
    "DATE": "date",
    "SKILL": "keywords",
    "COURSE": "courses",
    "none": "unlabeled",
}

CERTIFICATE = {
    "name": "Certificate",
    "date": "2021-11-07",
    "issuer": "Company",
    "url": "https://certificate.com",
}

CERTIFICATE_MAP = {
    "CERTIFICATE": "name",
    "COMPANY": "issuer",
    "ACADEMIC_ORG": "issuer",
    "DATE": "date",
    "none": "unlabeled",
}

SKILLS = {
    "name": "Web Development",
    "level": "Master",
    "keywords": ["HTML", "CSS", "JavaScript"],
}

REFERENCE = {"name": "Jane Doe", "reference": "Reference…"}
REFERENCE_MAP = {
    "PERSON_NAME": "name",
    "EMAIL": "email",
    "PHONE": "phone",
    "JOB_TITLE": "role",
    "ORG": "organization",
    "none": "unlabeled",
}

PROJECT = {
    "name": "Project",
    "highlights": ["Won award at AIHacks 2016"],
    "keywords": ["HTML"],
    "startDate": "2019-01-01",
    "endDate": "2021-01-01",
    "roles": ["Team Lead"],
}

PROJECT_MAP = {
    "PROJECT_NAME": "name",
    "DOING": "highlights",
    "SKILL": "keywords",
    "DATE": "date",
    "URL": "url",
    "JOB_TITLE": "roles",
    "none": "unlabeled",
}

HOBBY = {"name": "Wildlife", "keywords": ["Ferrets", "Unicorns"]}

HOBBY_MAP = {"HOBBY": "name"}
