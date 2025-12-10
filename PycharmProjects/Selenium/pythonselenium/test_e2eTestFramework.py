import json
import os
import sys

import pytest

from pageobjects.Shop import Shoppage

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pageobjects.loginpage import Loginpage
test_data_path = '../data/test_e2eTestFramework.json'
with open (test_data_path) as f:
    test_data = json.load(f)
    test_list = test_data["data"]


@pytest.mark.parametrize("test_list_item", test_list)
def test_e2e(browserinstance, test_list_item):
    driver = browserinstance
    driver.get("https://rahulshettyacademy.com/loginpagePractise/")
    #  //a[contains(@href,'shop')]    a[href*='shop']
    loginpage = Loginpage(driver)
    shop_page = loginpage.login(test_list_item["useremail"], test_list_item["userpassword"])
    shop_page.add_product_to_cart(test_list_item["productname"])
    checkout_confirmation = shop_page.gotocart()
    checkout_confirmation.checkout()
    checkout_confirmation.delivery_address("ind")
    checkout_confirmation.validate_Order()









