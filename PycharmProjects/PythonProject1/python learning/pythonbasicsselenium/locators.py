
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()

driver.get("http://www.rahulshettyacademy.com/angularpractice/")
#driver.get("https://www.apple.com/")



driver.maximize_window()

driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("sai")
driver.find_element(By.NAME, "email").send_keys("saitejaraj.guvvala@gmail.com")
driver.find_element(By.ID, "exampleInputPassword1").send_keys("1234")
dropdown = Select(driver.find_element(By.XPATH, "//select[@id='exampleFormControlSelect1']"))
dropdown.select_by_visible_text("Female")
driver.find_element(By.ID, "exampleCheck1").click()
driver.find_element(By.XPATH, "//input[@id = 'inlineRadio1']").click()

time.sleep(5)
