FROM nikolaik/python-nodejs:python3.8-nodejs17-slim

    WORKDIR /app
    COPY . /app/.

    #RUN apt-get update -y
    #RUN apt-get install libgtk2.0-0 -y
    #RUN npm install -g resume-cli
    #RUN npm install jsonresume-theme-even

    RUN pip install -U pip
    RUN pip install --no-cache-dir  -r requirements.txt

    CMD streamlit run app_online.py
