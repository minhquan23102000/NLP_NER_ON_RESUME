mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"minhquan23102000@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = ${PORT:-8501}\n\
" > ~/.streamlit/config.toml
