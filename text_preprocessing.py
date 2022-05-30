def clean_whitespace(statement):
    """
    Remove any consecutive whitespace characters from the statement text.
    """

    import re

    # Replace linebreaks and tabs with spaces
    statement = ' '.join(statement.split())

    # Remove any leading or trailing whitespace
    statement = statement.strip()

    # Remove consecutive spaces
    statement = re.sub('\s+', ' ', statement)

    return statement

def clean_text(text):
    import re

    from pyvi import ViUtils
    text = re.sub(r"[^'/\\&@.+#*%\w\d\s]", ' ', text)

    #remove accents
    text = ViUtils.remove_accents(text).decode('utf-8')
    text = clean_whitespace(text)

    return text
