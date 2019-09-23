import re

# For pattern and application see: https://is.gd/IPf2pL.

PATTERN = r"""(?x)
    ^
    \s*
    (?P<number>
        (?P<sign>[+-])?
        (?P<integer_part>
            \d{1,3}
            (?P<sep>
                [ ,.]
            )
            \d{3}
            (?:
                (?P=sep)
                \d{3}
            )*
        |
            \d+
        )?
        (?P<decimal_part>
            (?P<point>
                (?(sep)
                    (?!
                        (?P=sep)
                    )
                )
                [.,]
            )
            \d+
        )?
    )
    \s*[\.:ː]
"""


def parse_number(text):
    match = re.match(PATTERN, text)
    if match is None or not (
        match.group("integer_part") or match.group("decimal_part")
    ):
        raise ValueError("Couldn't find a number.")

    num_str = match.group("number")
    sep = match.group("sep")

    if sep:
        num_str = num_str.replace(sep, "")  # remove thousands separators

    if match.group("decimal_part"):
        point = match.group("point")
        if point != ".":
            # regularize decimal point
            num_str = num_str.replace(point, ".")
        return float(num_str)

    return int(num_str)
