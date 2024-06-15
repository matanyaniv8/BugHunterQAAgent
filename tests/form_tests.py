from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import base64


def setup_selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # For headless operation
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def load_html_content(driver, html_content):
    """Load HTML content into Selenium browser using data URL."""
    encoded_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    driver.get(f"data:text/html;base64,{encoded_html}")


def perform_tests(driver):
    """Perform form input and submission tests on the loaded content."""
    results = {}
    try:
        forms = WebDriverWait(driver, 10).until(
            lambda x: x.find_elements(By.TAG_NAME, "form") if x.find_elements(By.TAG_NAME, "form") else False
        )
    except TimeoutException:
        results['General Error'] = 'No forms found on the page or timeout reached'
        return results

    if not forms:
        results['General Error'] = 'No forms found on the page'
        return results

    for form_index, form in enumerate(forms):
        form_description = form.get_attribute('id') or f"Form {form_index + 1}"
        results[form_description] = {
            **test_input_fields(form),
            **test_form_submission(form, driver)
        }
    return results


def test_input_fields(form):
    """Test input fields within a form."""
    results = {}
    inputs = form.find_elements(By.CSS_SELECTOR, "input, textarea")
    for input in inputs:
        input_type = input.get_attribute("type") or input.tag_name
        input_name = input.get_attribute("name") or "Unnamed Input"
        test_description = f"{input.tag_name} {input_type} {input_name}"  # Descriptive name
        test_result = "passed - Filled or Checked"
        try:
            if input_type in ["text", "password", "email", "textarea"]:
                input.send_keys("test")
            elif input_type in ["checkbox", "radio"]:
                input.click() if not input.is_selected() else None
        except TimeoutException:
            if form is None:
                results = {}
        except StaleElementReferenceException:
            if form is None:
                results = {}
        except Exception:
            test_result = f"failed -  Failed to run test"
        results[test_description] = test_result
    return results


def get_button_text(button):
    # Try to get text directly from the button
    text = button.get_attribute('value').strip()
    if not text:
        # Try to get text from nested elements
        for element in button.find_elements(By.XPATH, ".//*"):
            text = element.text.strip()
            if text:
                break
    return text


def test_form_submission(form, driver):
    """Check form submission capability."""
    results = {}
    test_description = "Form Submission Test"
    try:
        submit_button = form.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        if submit_button:
            button_text = get_button_text(submit_button)
            submit_button.click()
            WebDriverWait(driver, 10).until(
                lambda x: driver.execute_script("return document.readyState === 'complete'"))
            results[test_description] = f"passed - Submitted, Button Text: {button_text}"
        else:
            results[test_description] = "failed - No Submit Button"
    except NoSuchElementException:
        results[test_description] = "failed - No Submit Button"
    except Exception:
        results[test_description] = f"failed -  Failed to run test"
    return results


def execute_forms_url_tests(url):
    """Load a URL and perform tests."""
    driver = setup_selenium_driver()
    driver.get(url)
    results = perform_tests(driver)
    driver.quit()
    return results


def execute_forms_html_tests(html_content):
    """Load HTML content and perform tests."""
    driver = setup_selenium_driver()
    load_html_content(driver, html_content)
    results = perform_tests(driver)
    driver.quit()
    return results
