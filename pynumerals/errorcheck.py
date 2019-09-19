
def _check_fullstop(value):
    """Checks whether there is a fullstop"""
    return "." in value


_checkers = [
     _check_fullstop,
     
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
