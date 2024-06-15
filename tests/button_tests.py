import base64
from selenium.common import StaleElementReferenceException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def setup_selenium_driver():
    """
    Sets up the selenium webdriver.
    :return:
        Loaded Driver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for automation environments
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


def perform_button_tests(driver):
    """
       Performs visibility, interactivity, and click tests on all button elements found on the webpage.

       Parameters:
       - driver (webdriver): Selenium WebDriver to interact with the webpage.

       Returns:
       - dict: Results for each button tested, detailing visibility, interactivity, and click outcomes.
       """
    results = {}
    try:
        # Wait until buttons are potentially loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                        "button, input[type='button'], input[type='submit'], input[type='reset'], a[role='button']")))
        # Select all elements that could be considered buttons
        buttons = driver.find_elements(By.CSS_SELECTOR,
                                       "button, input[type='button'], input[type='submit'], input[type='reset'], a[role='button']")
        print(len(buttons))
        if len(buttons) > 0:
            for index, button in enumerate(buttons):
                last_btn_tested = button
                button_text = button.text.strip() or button.get_attribute('title') or button.get_attribute(
                    'value') or "Unnamed Button"
                button_description = f"Button {index + 1}: {button_text}"  # Create a unique description for each button

                # Determine visibility
                visibility_test = "passed - Button is visible." if button.is_displayed() and button_text != "Unnamed Button" else "failed - Button is hidden."

                # Determine interactivity
                interact_test = "passed - Button is interactive." if button.is_enabled() else "failed - Button is not interactive."

                # Attempt to click the button if it's visible and interactive
                try:
                    if button.is_displayed() and button.is_enabled():
                        button.click()
                        # Example of checking for some JavaScript condition after click
                        if not driver.execute_script(
                                "return document.getElementById('expected-element-id') !== null"):
                            click_test = "failed - Expected element not found after click"
                        else:
                            click_test = "NOT ATTEMPTED - Button is not visible or not interactive."
                except Exception as e:
                    click_test = f"failed - {str(e)}"

                #         button.click()
                #         click_test = "PASSED - Button clicked without error."
                #     else:
                #         click_test = "NOT ATTEMPTED - Button is not visible or not interactive."
                # except Exception:
                #     click_test = f"FAILED - Error while clicking"

                results[button_description] = {
                    "Visibility Test": visibility_test,
                    "Interactivity Test": interact_test,
                    "Click Test": click_test
                }
    except StaleElementReferenceException:
        last_btn_tested = None
    except TimeoutException:
        last_btn_tested = None
    except Exception as e:
        print(type(e))
        results["General Error"] = f"FAILED - Failed to run test"
    return results


def execute_button_url_tests(url):
    """
    Opens in a selenium driver the url.
    """
    driver = setup_selenium_driver()
    try:
        driver.get(url)
        results = perform_button_tests(driver)
    finally:
        driver.quit()
    return results


def execute_button_html_tests(html_content):
    """
    Loads with selenium the HTML content.
    """
    driver = setup_selenium_driver()
    try:
        # load the html into the driver
        encoded_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        driver.get(f"data:text/html;base64,{encoded_html}")
        results = perform_button_tests(driver)

    finally:
        driver.quit()

    return results
