import re

def value_parser(value):

    other_form = None
    loan = False
    val = re.sub(r'\s*\*+$', '', value.strip()) # remove trailing *

    # replace Charis SIL PUA characters
    val = val.replace("","\u1DC4") # U+F171 -> COMBINING MACRON-ACUTE
    val = val.replace("","\u1DC5") # U+F172 -> COMBINING GRAVE-MACRON
    val = val.replace("","\u1DC6") # U+F173 -> COMBINING MACRON-GRAVE
    val = val.replace("","\u1DC7") # U+F174 -> COMBINING ACUTE-MACRON
    val = val.replace("","ꜛ") # U+F19C
    val = val.replace("","ꜜ") # U+F19D
    val = val.replace("","ȼ") # U+F20B
    val = val.replace("","ᵬ") # U+F249
    val = val.replace("","ᵭ") # U+F24A

    # actually: MODIFIER LETTER SMALL RAMS HORN - no Unicode code point yet
    # found in language Kodia only
    val = val.replace("","ɤ") # U+F1B5

    if len(val) > 2:
        if val[0] == '[' and val[-1] == ']':
            val = val[1:-1]
        # [foo] should be IPA represenation, everything in front of move to other_form (standard orthography)
        if '[' in val and not 'IPA' in val and not '=' in val and not '[lit' in val:
            m = re.search(r'(.*?)\s*\[([^\[\d]*?)\](.*)', val)
            if m:
                m = list(m.groups())
                if len(m) == 3:
                    val = "%s %s" % (m[1], m[2])
                    other_form = m[0]

    # everything after [ or ( or { is considered as being a comment
    # if it ends on counterpart - stuff like foo(b) will be ignored
    comment = ''
    for sep in [['[',']','?'], ['(',')',''], ['{','}','']]:
        s = re.compile("^(.*%s)\%s([^\%s]{2,}|[A-Z])\%s([\s\?\+\d]*)$" % (sep[2], sep[0], sep[0], sep[1]))
        m = s.search(val)
        if m:
            stack = 0
            for i, c in enumerate(val[::-1]):
                if c == sep[1]:
                    stack -= 1
                elif c == sep[0]:
                    stack += 1
                    if stack == 0:
                        break
            comment = val[len(val)-i-1:].strip()
            val = val[0:(len(val)-i-1)].strip()
    # comment phase 2
    m = re.search(r'^(.*?)\s+(\(.*?\))\s*$', val)
    if m:
        val = m.groups()[0].strip()
        comment = "%s %s" % (comment, m.groups()[1].strip())
        comment = comment.strip()

    # check for loans
    if comment:
        loan = bool(re.match(r'.*<\s*[A-Z]', comment)) # lgs starts with capital letter
        com = [comment]
    else:
        com = []
    if not loan:
        # < indicates loan word and move it to comment
        m = re.split(r'\s*<\s*(?=([A-Z]|from|borrow|loan))', val)
        if m and len(m) > 1:
            val = m[0]
            if len(m) == 3:
                com.append("< %s " % (m[2]).strip())
            else:
                com.append("< %s " % (" < ".join(m[2::2])).strip())
            loan = True

    val = re.sub(r'\s*[\*<]+$', '', val.strip()) # remove trailing *, <
    val = re.sub(r' {2,}', ' ', val)

    comment = ', '.join(com)
    # comment phase 3
    m = re.search(r'^(.*?)\s+(\(.*?\))\s*$', val)
    if m:
        val = m.groups()[0].strip()
        comment = "%s %s" % (comment, m.groups()[1].strip())
        comment = comment.strip()

    val = re.sub(r'\s*\(\s*$', '', val).strip()


    return val, comment, other_form, loan
