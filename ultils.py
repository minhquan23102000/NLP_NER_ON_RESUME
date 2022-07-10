
def parse_url(url:str):
    profile = {'url': url}
    if 'github' in url:
        profile['network'] = 'Github'
    elif 'twitter' in url:
        profile['network'] = 'Twitter'
    elif 'facebook' in url or 'fb' in url:
        profile['network'] = 'Facebook'
    elif 'linkedin' in url:
        profile['network'] = 'Linkedin'
    return profile

def format_date(date_str):
    from dateutil import parser
    if date_str.lower() in ['present', 'now']:
        return ""

    try:
        date = parser.parse(date_str)
        date_format = f"{date.year}-{date.month}-{date.day}"
    except Exception as e:
        print(str(e), e.__cause__)
        date_format = date_str

    return date_format

def buffer2base64(file_buffer):
    import base64

    return base64.b64encode(file_buffer).decode('utf-8')
