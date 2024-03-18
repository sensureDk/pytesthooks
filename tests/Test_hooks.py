import time

import pytest


def test_caseone():

    time.sleep(5)


def test_casetwo():
    pass


def test_casethree():
    pass


def test_fail():
    assert 1 == 2


def test_five():
    assert 1 == 1 / 0
