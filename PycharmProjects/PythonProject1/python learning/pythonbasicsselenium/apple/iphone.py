
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


driver = webdriver.Chrome()
driver.get("https://www.apple.com/")
driver.maximize_window()
wait = WebDriverWait(driver, 15)

store = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@class = 'globalnav-submenu-trigger-item']//a[@data-analytics-title = 'store']")))
store.click()

mac = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/shop/buy-mac'][normalize-space()='Mac']")))
mac.click()

macbook_pro = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-trigger-click='click [data-relatedlink=':ra:']]/div/a[@class='rf-hcard-cta button']")))
macbook_pro.click()
''''
action = ActionChains(driver)

action.move_to_element(store).pause(3).perform()
driver.quit()


try:
    submenu = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@data-analytics-region = 'explore shop']//ul[contains(@class,'globalnav-submenu-list')]")))
    print("Submenu is shown")
except:
    print("Submeni is not working")



time.sleep(4)
driver.save_screenshot("store_screenshot.png")
print("2. Screenshot saved")

'''
time.sleep(5)
driver.quit()


           