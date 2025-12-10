from selenium.webdriver.common.by import By

from pageobjects.checkout_confirmation import Checkout_Confirmation


class Shoppage:
    def __init__(self, driver):
        self.driver = driver
        self.shop_link = (By.CSS_SELECTOR, " a[href*='shop']")
        self.product_cards = (By.XPATH, "//div[@class='card h-100']")
        self.checkout = (By.CSS_SELECTOR, "a[class*='btn-primary']")


    def add_product_to_cart(self,product_name):
        self.driver.find_element(*self.shop_link).click()
        products = self.driver.find_elements(*self.product_cards)

        for product in products:
            productName = product.find_element(By.XPATH, "div/h4/a").text
            if productName == product_name:
                product.find_element(By.XPATH, "div/button").click()


    def gotocart (self):
        self.driver.find_element(*self.checkout).click()
        checkout_confirmation = Checkout_Confirmation(self.driver)
        return checkout_confirmation


