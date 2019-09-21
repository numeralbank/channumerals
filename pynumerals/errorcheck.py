import re

def error_fullstop(value):
    """Checks whether there is a fullstop after a digit"""
    return bool(re.match(r'.*\d+\.', value))


def error_loanword(value):
    """Checks whether the item is an unidentified loanword"""
    return '<' in value


def error_is_numeric(value):
    """Checks if the value is only numerical"""
    try:
        int(value)
        return True
    except:
        return False


def error_has_numeric(value):
    """Checks if the value has a space followed by a digit"""
    return bool(re.match(r'.* \d', value))


def error_has_abbr(value):
    """Checks if the value has a single char followed by a fullstop and a space"""
    return bool(re.match(r'.*\b.\. ', value))


def error_has_parenthesis(value):
    """Checks if the value has a single ) or ("""
    return bool(')' in value and not '(' in value) or bool('(' in value and not ')' in value)


def error_has_gloss(value):
    """Checks if the value has at least a hyphen followed by two capital letters"""
    return bool(re.match(r'.*\-[A-Z]{2,}', value))


_blacklist = [
    ' or ', ' also ', '[', ']', '>', '{', '}', ' = ', '?', '..', '+', ' ‘', '*', '~', '/', '→',
    'lit.', 'lit:', 'litː', 'litt.', 'litt:', 'literally', ' are ', ' is a ', ' hand ', ' hands', ' feet ', ' foot ',
    ' x ', '. ', 'borrow', 'numeral', 'used', 'other', 'number', 'used ', 'formerly', 'complex', 'from ',
    'only', 'morph', 'which', ' not ', 'mean', 'note', 'probably', 'finger', 'animate', 'masc', 'femin', 'fem.',
    'missing', 'Ø', 'elbow', 'joint', "'and'", 'alternative', 'midway', 'lower',
    'english', 'french', 'german', 'spanish', 'portuguese', 'sanskrit', 'dutch', 'quechua',
    'arabic', 'hinid', 'chinese', 'tok pisin', 'swahili', 'bislama'
]
_blacklistCS = [
    'IPA'
]
_blacklistIS = [
    '-', "'", 'k', '́'
]
def error_has_blacklist_item(value):
    v = value.lower()
    for b in _blacklist:
        if b in v:
            return True
    for b in _blacklistCS:
        if b in value:
            return True
    for b in _blacklistIS:
        if b == value:
            return True
    return False


errorchecks = [
     error_fullstop,
     error_has_blacklist_item,
     error_loanword,
     error_is_numeric,
     error_has_numeric,
     error_has_abbr,
     error_has_gloss,
     error_has_parenthesis,
]
