# coding: utf-8
from __future__ import unicode_literals

from pynumerals.errorcheck import error_fullstop
from pynumerals.errorcheck import error_loanword
from pynumerals.errorcheck import error_is_numeric
from pynumerals.errorcheck import error_is_language
from pynumerals.errorcheck import error_or


def test_error_fullstop():
    assert error_fullstop("1. lima")
    assert not error_fullstop("lima")
    assert not error_fullstop("li.ma")


def test_error_loanword():
    assert error_loanword("lima <Tongan")
    assert not error_loanword("lima")


def test_error_is_numeric():
    assert error_is_numeric("5")
    assert not error_is_numeric("lima")


def test_error_is_language():
    assert error_is_language("English")
    assert not error_is_language("lima")


def test_error_or():
    assert error_or("lima or rima")
    assert not error_or("lima")
    assert not error_or("liorma")

