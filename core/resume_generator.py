import subprocess

#from weasyprint import HTML

RESUME_HTML_PATH = 'resume.html'

def generate_resume(theme:str):
    generate_resume_command = f"npx resumed render -t {theme}"
    output = subprocess.check_call(generate_resume_command, shell=True)

    with open(RESUME_HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    return html
