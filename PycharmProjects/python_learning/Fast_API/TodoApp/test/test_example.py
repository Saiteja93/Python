import pytest


def test_number_equals_or_not():
    assert  3 == 3
    assert 3 != 1

def test_is_instance():
    assert isinstance('this is string',str)
    assert not isinstance('10', int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' =='world') is False

def test_type():
    assert type('hello' is str)
    assert type('hello' is not int)


