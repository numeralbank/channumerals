
def _check_fullstop(value):
    """Checks whether there is a fullstop"""
    return "." in value


def _check_loanword(value):
    """Checks whether the item is an unidentified loanword"""
    return '>' in value



_checkers = [
     _check_fullstop,
     _check_loanword,
     
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
