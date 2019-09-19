
def _check_fullstop(value):
    """Checks whether there is a fullstop"""
    return "." in value


def _check_loanword(value):
    """Checks whether the item is an unidentified loanword"""
    return '>' in value


def _check_is_language(value):
    """Checks if the value points to another language"""
    return value.lower in ['english', 'french', 'german', 'spanish', 'portuguese']


def _check_is_numeric(value):
    """Checks if the value is only numerical"""
    try:
        int(value)
        return True
    except:
        return False


def _check_or(value):
    return ' or ' in value


_checkers = [
     _check_fullstop,
     _check_loanword,
     _check_is_numeric,
     _check_is_language,
     _check_or,
]


def check(value):
    """
    Error Checking function.
    
    Returns True if the entry is flagged as problematic
    """
    for c in _checkers:
        if c(value):
            return True
    return False
