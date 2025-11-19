import pytest

from pytestDemo.conftest import setup


@pytest.mark.usefixtures("setup")
class Testexample:
    def test_fixturedemo1(self):
        print ("i will be executing first method")

    def test_fixturedemo2(self):
        print("i will be executing second method")

    def test_fixturedemo3(self):
        print("i will be executing third method")

    def test_fixturedemo4(self):
        print("i will be executing fourth method")