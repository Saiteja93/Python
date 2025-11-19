from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
driver.get("https://www.apple.com/")
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# 1️⃣ Hover over the header "Store" menu (<li>)
store_li = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//li[@class="globalnav-submenu-trigger-item"][//a[@data-analytics-title="store"]]')
))
actions = ActionChains(driver)
actions.move_to_element(store_li).pause(2).perform()  # pause allows animation

# 2️⃣ Wait for submenu to exist in DOM (not necessarily visible yet)
submenu = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//ul[@class="globalnav-submenu-list"]')
))
time.sleep(1)  # give CSS animation a moment

# 3️⃣ Take screenshot of the full page (includes dropdown)
driver.save_screenshot("store_dropdown.png")
print("✅ Screenshot saved as store_dropdown.png")

# 4️⃣ Click the "iPad" link
ipad_link = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//ul[@class="globalnav-submenu-list"]//a[@data-analytics-title="ipad"]')
))
driver.execute_script("arguments[0].click();", ipad_link)

# 5️⃣ Wait for iPad page to load by checking heading
ipad_heading = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//h1[contains(text(),'iPad')]")
))
print("✅ iPad page loaded successfully:", ipad_heading.text)

time.sleep(3)
driver.quit()
