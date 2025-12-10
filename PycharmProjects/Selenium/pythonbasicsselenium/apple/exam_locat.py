from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.apple.com/")

wait = WebDriverWait(driver, 10)
ipad_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='iPad']")))

print("Found element:", ipad_link.text)
ipad_link.click()

driver.quit()
