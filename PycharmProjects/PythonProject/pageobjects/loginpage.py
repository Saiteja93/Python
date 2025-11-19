from selenium.webdriver.common.by import By

from pageobjects.Shop import Shoppage


class Loginpage:
    def __init__(self, driver):
        self.driver = driver
        self.useremail_field = By.ID, "username"
        self.userpassword_field = By.NAME, "password"
        self.signbutton = By.ID, "signInBtn"



    def login(self, useremail, userpassword):
        self.driver.find_element(*self.useremail_field).send_keys(useremail)
        self.driver.find_element(*self.userpassword_field).send_keys(userpassword)
        self.driver.find_element(*self.signbutton).click()
        shop_page = Shoppage(self.driver)
        return shop_page
