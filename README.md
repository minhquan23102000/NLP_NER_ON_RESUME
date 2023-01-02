# NLP_NER_ON_RESUME
Using spacy transformer to train NER model on resume dataset

# Note
This is a labotory to known how to build a ner model on resume dataset. To build a extract system that meet the actual needs is need much more steps of combination of algorithm such as rule-base matching, regular expressions, etc. You can view more detail in application branch of this repo.

# Demo
### Streamlit app

![ezgif-4-5339088822](https://user-images.githubusercontent.com/57226852/210192175-9fdf942c-362b-4a7d-9074-f5d5852f0344.gif)


### Run on terminal after train spacy ner model
```cmd
python .\demo.py --resume_path '.JuniorDataScientist_NGUYỄN MINH QUÂN.pdf'
```

**The parsing result will follow json resume schema** you can view from this link: https://jsonresume.org/schema/

### Output
```
{
  "basics": {
    "profiles": [
      {
        "url": "linkedin.com/in/quan-minh/073265224/",
        "network": "Linkedin"
      },
      {
        "url": "github.com/minhquan23102000",
        "network": "Github"
      }
    ],
    "location": {
      "address": "Go  Vap Ho  Chi  Minh"
    },
    "name": "NGUYE  N  MINH  QUA  N",
    "other": "JUNIOR  DATA  SCIENTIST",
    "phone": "+84  383666401",
    "email": "minhquan23102000@gmail.com",
    "summary": "\nI'm a Data Scientist with an IT background and strong in problem-solving. I have experience in SQL, NLP,\ndata science pipeline, machine learning, and deep learning. I have over one year of experience in\nimplementing data science projects such as building predicting models, text classification, dashboards,\nrecommendation systems, time series analysis, customer segment, human face recognition, name\nentities recognition, Chatbot…\n\nDuring my study, I published two research papers about Chatbot at the HUTECH science conference\n2022 and JTIN journal article. As an AI software startup project, I also won the most impressive prize in\nthe HUTECH Startup Wings 2022. Currently, I have been chosen as one of five technology research\nteams to join the EUREKA competition.\n\n\n\nShort-term: find a good environment to gain more experience in embracing fields such as Data Scientist\nand AI Engineer.\nLong-term: to become a senior data scientist in 3-5 years.",
    "label": "JUNIOR  DATA  SCIENTIST"
  },
  "education": [
    {
      "startDate": "2018-1-2",
      "endDate": "2022-1-2",
      "unlabeled": "Calculus",
      "institution": "B.E  INFORMATION  TECHNOLOGY UNIVERSITY  OF  TECHNOLOGY  HUTECH",
      "score": "3.30/4.0",
      "keywords": "Data  structures",
      "date": "2020-1-2"
    },
    {
      "institution": "I.C  DATA  SCIENCE  APPLIED",
      "unlabeled": "Courses",
      "score": "3.88/4.0",
      "keywords": "Big  Data",
      "startDate": "2020-1-2"
    }
  ],
  "certificates": [],
  "interests": [],
  "skills": [
    {
      "name": "Key skills",
      "keywords": [
        "Computer  Vision",
        "OOP",
        "English",
        "Presentation",
        "Tensorflow",
        "Data  Analysis",
        "Pandas",
        "Github",
        "Keras",
        "Statistics",
        "Heroku",
        "Teamwork",
        "PROGRAMMING",
        "Python",
        "Data  Visualization",
        "Machine  Learning",
        "OpenCV",
        "Docker",
        "SQL",
        "Flask",
        "Java",
        "Data  Science",
        "Numpy",
        "Deep  Learning",
        "Pytorch",
        "Plotly",
        "Communication"
      ]
    }
  ],
  "work": [
    {
      "startDate": "2022-5-2",
      "endDate": "2022-8-2",
      "unlabeled": "FPT  INFORMATION  SYSTEM \n\n Collect  and  label  CVs  dataset help  the  company  have  valuable  data  on",
      "name": "INTERN  DATA  SCIENTIST  NLP",
      "highlights": [
        "Developing machine  model  for  resumes  handling  business",
        "Implement  a  bot  that  can  read  resumes help  the  HR  department",
        "Automatically  filter resumes  and  insert  candicates  information  to  database"
      ],
      "date": "2021-9-2"
    },
    {
      "name": "AI  STUDENT  RESEARCHER",
      "highlights": [
        "Research  and  implement  Chatbot  for  automotive  guide  people  doing  administrative documents while",
        "Ensuring  the  continuation  and  enhancements  of  services",
        "Join  the  final  round  of  Hutech  Startup  Wings  as  an  AI  startup  product  and  won  the  most impressive  project  prize"
      ],
      "startDate": "2021-9-2",
      "endDate": "2020-4-2",
      "date": "2021-7-2"
    },
    {
      "name": "DATA  SCIENTIST  STUDENT",
      "highlights": [
        "Hand  on  prediction  models  big  data  such  as  price  regression text  classification  using  Decision Tree KNN Random  forests SVM Naive  Bayes XGBoost ... \n\n recommendation  system  and  preprocessing  using  PySpark  library",
        "Hand  on  time  series  analysis  Fbprophet SARIMA and  customer  segmentation  using Kmean GMM DBScan"
      ],
      "startDate": "2021-7-2"
    }
  ],
  "projects": [],
  "references": []
}
```

### You can view more demo detail from this link: https://readyourresume.herokuapp.com/ 
or docker hub, if the web app not avaible: https://hub.docker.com/repository/docker/minhquan23102000/cv_reader

# Train model
## Step 0: Prepare environment
Because using BERT to train model, so we need a GPU.

Clone this project.

Then run
```cmd
pip install -r requirement.txt
```

Make sure you have an available GPU (with Dedicated GPU memory >= 3.0 GB). Also installed CUDA on your device


## Step 1: Run prepare_data.py to create train and val corpus
```cmd
python prepare_data.py
```
## Step 2: Edit config.cfg file to match your environment
```
[components.transformer.model]
@architectures = "spacy-transformers.TransformerModel.v3"
name = "distilroberta-base"
mixed_precision = fals
```
You can change BERT name model with the atr 'name' above, at here I use DistilRoberta-base. You can view and select model at here: https://huggingface.co/distilroberta-base

```
[training.batcher]
@batchers = "spacy.batch_by_padded.v1"
discard_oversize = false
size = 256 
buffer = 128 
get_length = null
```
Increase training.batcher size to speed up training process, but will consume memory.
More config you can read at spacy document: https://spacy.io/usage/training#config

## Step 3: Start traning
```cmd
python -m spacy train config.cf
```

## Step 4: Evaluation

### Model train after 45 epoch
![image](https://user-images.githubusercontent.com/57226852/170948579-4d11785e-bf96-40e4-b4f4-a9256cc2421a.png)



