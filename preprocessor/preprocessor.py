def remove_accents(s):
    import re
    import unicodedata
    s = re.sub('\u0110', 'D', s)
    s = re.sub('\u0111', 'd', s)
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')
def clean_whitespace(statement):
    """
    Remove any consecutive whitespace characters from the statement text.
    """

    import re

    # Replace linebreaks and tabs with spaces
    #statement = ' '.join(statement.split())
    # Remove any leading or trailing whitespace
    statement = statement.strip()

    # Remove consecutive spaces
    #Simplify multiple line break, tab, or space
    statement = re.sub(r'\r\n', '\n', statement)
    statement = re.sub(r'\n{3,}', '\n\n', statement)
    statement = re.sub(r' {2,}', ' ', statement)
    statement = re.sub(r'\t{2,}', '\t', statement)

    return statement


def clean_text(text):
    import re

    #remove accents
    text = remove_accents(text).decode('utf-8')

    #remove continuos characters
    text = re.sub(r'[^\w\d\s]{4,}', ' ', text)

    #clean white space
    text = clean_whitespace(text)

    return text
