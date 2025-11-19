from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Helper for robust WebDriver setup (optional, but good practice)
try:
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WDM = True
except ImportError:
    USE_WDM = False

def run_apple_test():
    """
    Navigates to apple.com, hovers over the 'Store' link to capture the 
    mega-menu screenshot, then clicks 'iPad' to verify navigation.
    """
    driver = None
    try:
        # 1. Setup WebDriver
        if USE_WDM:
            # Uses webdriver_manager to automatically download the correct driver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        else:
            print("Note: 'webdriver_manager' not found. Assuming chromedriver is in PATH.")
            driver = webdriver.Chrome()

        print("Starting Apple navigation and testing sequence (Store Menu)...")

        driver.get("https://www.apple.com/")
        driver.maximize_window()
        # Explicit wait object for maximum of 15 seconds
        wait = WebDriverWait(driver, 15)

        # 1️⃣ Hover over the header "Store" menu (<li>)
        print("1/5: Hovering over 'Store' menu...")
        store_li = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//li[contains(@class,"globalnav-submenu-trigger-item")][//a[@data-analytics-title="store"]]')
        ))
        actions = ActionChains(driver)
        # Move to the element and pause for 2 seconds to allow the CSS animation to complete
        actions.move_to_element(store_li).pause(5).perform()

        # 2️⃣ Wait for submenu to exist in DOM and be visible
        print("2/5: Waiting for mega-menu to fully appear...")
        
        # --- FIX: Using the specific CSS selector for the Store menu ---
        # This selector targets the list inside the unique wrapper for the 'Store' menu.
        submenu_selector = "//div[@data-analytics-region='explore shop']//ul[@class='globalnav-submenu-list']"
        submenu = wait.until(EC.presence_of_element_located(
            (By.XPATH, submenu_selector)
        ))
        
        # Wait a moment for visual completeness before screenshot
        wait.until(EC.visibility_of(submenu))
        time.sleep(4)
        print("2/5: ✅ Mega-menu is visible.")

        # 3️⃣ Take screenshot of the full page (includes dropdown)
        screenshot_filename = "store_dropdown.png"
        driver.save_screenshot(screenshot_filename)
        print(f"3/5: ✅ Screenshot saved as '{os.path.abspath(screenshot_filename)}'")

        # 🛑 Re-hover to prevent the menu from collapsing
        print("3.5/5: Re-hovering over 'Store' to keep the mega-menu active.")
        actions.move_to_element(store_li).perform()
        
        # 4️⃣ Click the "iPad" link
        print("4/5: Clicking the 'iPad' link...")
        ipad_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//ul[@class="globalnav-submenu-list"]//a[@data-analytics-title="ipad"]')
        ))
        # Use execute_script for a robust click
        driver.execute_script("arguments[0].click();", ipad_link)

        # 5️⃣ Wait for iPad page to load by checking for the main heading
        print("5/5: Waiting for iPad page to load and verifying heading...")
        ipad_heading = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'iPad')]")
        ))
        print(f"✅ SUCCESS: Navigation successful. Heading found: {ipad_heading.text}")

    except Exception as e:
        print(f"\nFAILURE: An error occurred during the test: {e}")
        if driver:
            print(f"Current URL on failure: {driver.current_url}")

    finally:
        # 6. Quit the browser gracefully
        if driver:
            time.sleep(1)
            driver.quit()
            print("\nBrowser closed.")

if __name__ == "__main__":
    run_apple_test()
