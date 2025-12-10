import pytest


@pytest.mark.smoke
def test_firstprogram():
    print("hello how are you")

@pytest.mark.xfail
def test_secondprogram():
    print("Good morning")

