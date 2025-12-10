import pytest


@pytest.fixture(scope ="class")
def setup():
    print ("i will be executing first")
    yield
    print(" i will be executing last ")

@pytest.fixture()
def dataload():
    print ("This is the data")
    return ["sai","teja","saiteja@gmail.com"]

@pytest.fixture(params=[("chrome", "sai", "hima"), ("firefox", "teja", "himaja")])
def crossBrowser(request):
    return request.param


