import pytest


@pytest.mark.usefixtures("dataload")
class TestExample2:

    def test_editprofile(self, dataload):
        print (dataload[1])
        print (dataload)
        print (dataload[0])




