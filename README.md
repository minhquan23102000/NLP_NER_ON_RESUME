# NLP_NER_ON_RESUME
Using spacy transformer to train NER model on resume dataset

# Note
This is a labotory to known how to build a ner model on resume dataset. To build a extract system that meet the actual needs is need much more steps of combination of algorithm such as rule-base matching, regular expressions, etc. You can view more detail in application branch of this repo.

# Demo
### Run on terminal after train spacy ner model
```cmd
python .\demo.py --resume_path '.\resource\CV\IT\Front End\Le Tan Nghia (Senior Front-end).pdf'
```
### Output
```
PERSON_NAME: [{'Nguyen Van Mot', 'Le Tan Nghia', 'Tran Nguyen Khai', 'Nghia Tan Le', 'Nguyen Xuan Manh'}]
DATE_BIRTH: [{'23-8-1981', '6-11-2007'}]
GENDER: [{'Male'}]
LOCATION: [{'Don Duong Lam', 'Dong Nai Province'}]
ADDRESS: [{'1/17 Su Van Hanh Street Ward 12 Distrit 10 HCMC', '242 Nguyen Kiem Street Go Vap District HCMC', '4th Floor Le Tri Building 164B Phan Van Tri Street Ward 12 Binh Thanh District Ho Chi Minh City', '115 Nguyen Hue Street Distrit 1 HCMC', '71/15 Nguyen Phuc Chu Street 15 Ward Tan Binh District HCMC', 'E27 billet 304 307 D1 Street Ward 25 District Binh Thanh HCMC'}]
MARIAGE_STATUS: [{'Single'}]
EXPERIENCE_LEVEL: [{'Experience 9 years', 'five years relevant'}]
MAJOR: [{'Computer & Telecommunication', 'IT'}]
SKILL: [{'HTML', 'Safari', 'HTML & CSS', 'Netscape4', 'Mysql', 'CSS', 'Opera', 'Swish', 'FPT', 'CMS driven', 'JavaScript development', 'Fireworks', 'graphic design', 'web design', 'Net', 'communication', 'Coding', 'testing', 'Jquery', 'Dreamweaver', 'XHTML', 'Photoshop', 'IE6', 'Mac', 'Flash', 'SEO', 'Software and code', 'SQL', 'MS Office', 'visual design', 'X', 'ActionScript', 'Ftp', 'Flash banner', 'PHP', 'HTML coding', 'web usability', 'Javascript', 'web marketing', 'design ideas', 'MySQL', 'W3C', 'Autocad', 'Dot', 'Web usability', 'CorelDRAW', 'Search Engine Optimization', 'Ubuntu', 'Web content optimization', 'JavaScript', 'Web Design'}]
JOB_TITLE: [{'Mobi', 'web designer', 'Project Manager', 'Manager', 'web developer', 'Web Developer', 'Web designer', 'Web Design', 'Web developer'}]
ORGANIZATION: [{'UNI SYS Ltd', 'IMJ Corporation', 'Freelance', 'Yakobonde Co. Ltd.', 'Victory Data Solutions company', 'UNI SYS company', 'Thanexys Co. Ltd.', 'Grafight VN Corporation'}]
EMAIL: [{'nghiaweb@gmail.com', 'nghiaweb@yahoo.com'}]
PROFILE_URL: [{'anhsangvang.com.vn', 'ruellevietnam.com', 'www.khavitech.com', 'ngoinhavip.com.vn', 'pmgallnatural.com/', 'www.hoatuoihuythao.com/', 'www.vietnamgeeks.com', 'thanexys.com', 'deco.fr'}]
PHONE: [set()]
```

### You can view more demo detail from this link: https://readyourresume.herokuapp.com/ 

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



