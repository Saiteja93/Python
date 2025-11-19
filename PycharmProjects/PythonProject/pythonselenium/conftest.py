import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="my option for web browser"
    )


@pytest.fixture(scope='function')
def browserinstance(request):
    browser_name = request.config.getoption('browser_name')
    service_obj = Service()
    if browser_name == 'chrome':
        driver = webdriver.Chrome(service=service_obj)

    elif browser_name == 'firefox':
        driver = webdriver.Firefox(service=service_obj)

    driver.implicitly_wait(5)

    yield driver
    driver.close()










