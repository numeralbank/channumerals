# coding: utf-8
from __future__ import unicode_literals

from pynumerals.errorcheck import errorchecks

good_ones = ["lima", "li.ma", "liorma"]
bad_ones = ["1. lima", "lima <Tongan", "5", "English", "lima or rima"]

for s in good_ones:
    r = False
    for check in errorchecks:
        if check(s):
            r = True
            break
    assert not r

for s in bad_ones:
    r = False
    for check in errorchecks:
        if check(s):
            r = True
            break
    assert r

