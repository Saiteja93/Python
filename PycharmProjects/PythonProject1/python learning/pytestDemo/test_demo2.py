import pytest


@pytest.mark.smoke
@pytest.mark.skip
def test_firstprogram():
    mssg = "hello"
    assert mssg == "hi" , "test failed due to not matching"

def test_secondCreditCard():
    a = 12
    b = 13
    assert a+b == 25



def test_fixtureDemo(setup):
    print(" i will execute first in fixturedemo ")


def test_crossBrowser(crossBrowser):
    print (crossBrowser[1])
