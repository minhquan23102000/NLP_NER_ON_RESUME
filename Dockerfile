FROM nikolaik/python-nodejs:python3.8-nodejs17-slim

    WORKDIR /app
    COPY . /app/.

    RUN pip install -U pip
    RUN pip install --no-cache-dir  -r requirements.txt

    CMD streamlit run app_online.py --server.port ${PORT:-8501} --server.headless true
