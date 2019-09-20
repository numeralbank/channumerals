import re

def error_fullstop(value):
    """Checks whether there is a fullstop after a digit"""
    return bool(re.match(r'.*\d+\.', value))


def error_loanword(value):
    """Checks whether the item is an unidentified loanword"""
    return '<' in value


_languages_to_check = [
    'english', 'french', 'german', 'spanish', 'portuguese', 'sanskrit', 'dutch'
]

def error_is_language(value):
    """Checks if the value points to another language"""
    return value.lower() in _languages_to_check


def error_is_numeric(value):
    """Checks if the value is only numerical"""
    try:
        int(value)
        return True
    except:
        return False


def error_or(value):
    return ' or ' in value


errorchecks = [
     error_fullstop,
     error_loanword,
     error_is_numeric,
     error_is_language,
     error_or,
]