FROM nikolaik/python-nodejs:python3.8-nodejs17-slim

    WORKDIR /app
    COPY . /app/.

    RUN npm install -g resume-cli

    RUN pip install -U pip
    RUN pip install --no-cache-dir  -r requirements.txt

    CMD sh setup.sh && streamlit run app_online.py
