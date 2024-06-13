from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
    forms = driver.find_elements(By.TAG_NAME, "form")
    if len(forms) > 0:
        for form_index, form in enumerate(forms):
            form_id = form.get_attribute('id') or f"Form {form_index + 1}"
            results[form_id] = {}
            results[form_id].update(test_input_fields(form))
            results[form_id].update(test_form_submission(form, driver))
    return results


def test_input_fields(form):
    """Test input fields within a form."""
    results = {}
    inputs = form.find_elements(By.CSS_SELECTOR, "input, textarea")
    for input in inputs:
        input_type = input.get_attribute("type") or input.tag_name
        input_name = input.get_attribute("name") or "Unnamed Input"
        test_name = "Input Field Test"
        if input_type in ["text", "password", "email", "textarea"]:
            input.send_keys("test")
        elif input_type in ["checkbox", "radio"]:
            input.click() if not input.is_selected() else None
        results[f"{input.tag_name} {input_type} {input_name}"] = {test_name: "PASSED - Filled or Checked"}
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
    try:
        submit_button = form.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        if submit_button:
            button_text = get_button_text(submit_button)
            submit_button.click()
            # Use JavaScript to ensure that any AJAX or JS events triggered by the form submission are completed
            WebDriverWait(driver, 10).until(
                lambda x: driver.execute_script("return document.readyState === 'complete'"))
            results["Form Submission"] = {"Outcome": "PASSED - Submitted", "Button Text": button_text}
        else:
            results["Form Submission"] = {"Outcome": "FAILED - No Submit Button", "Button Text": "N/A"}
    except Exception as e:
        results["Form Submission"] = {"Outcome": f"FAILED - Exception: {str(e)}", "Button Text": "N/A"}
    return results


def test_url(url):
    """Load a URL and perform tests."""
    driver = setup_selenium_driver()
    driver.get(url)
    results = perform_tests(driver)
    driver.quit()
    return results


def test_html(html_content):
    """Load HTML content and perform tests."""
    driver = setup_selenium_driver()
    load_html_content(driver, html_content)
    results = perform_tests(driver)
    driver.quit()
    return results


if __name__ == "__main__":
    url = 'https://www.mako.co.il/collab/N12_Contact.html?partner=NewsfooterLinks&click_id=telDawcOaZ'
    html_con = "<html><body><form><input type='text'/><input type='submit'/></form></body></html>"

    # # Test with URL
    # print("Testing with URL:")
    # url_results = test_url(url)
    # print(url_results)
    # for k, v in url_results.items():
    #     print(f"{k}: {v}")
    # Test with HTML content
    print("\nTesting with HTML content:")
    html_results = test_html(html_con)
    print(html_results)
