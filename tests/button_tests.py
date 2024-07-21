from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException
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
        return results

    if not forms:
        return results

    for form_index, form in enumerate(forms):
        form_description = form.get_attribute('id') or f"Form {form_index + 1}"
        form_html = form.get_attribute('outerHTML')
        form_results = {
            **test_input_fields(form),
            **test_form_submission(form, driver)
        }

        buttons = form.find_elements(By.CSS_SELECTOR, "button, input[type='button'], input[type='submit']")
        for index, button in enumerate(buttons):
            button_html = button.get_attribute('outerHTML')
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
                    if not driver.execute_script("return document.getElementById('expected-element-id') !== null"):
                        click_test = "failed - Expected element not found after click"
                    else:
                        click_test = "passed - Button clicked and expected element found."
                else:
                    click_test = "NOT ATTEMPTED - Button is not visible or not interactive."
            except Exception as e:
                click_test = f"failed - {str(e)}"

            form_results[button_description] = {
                "Visibility Test": visibility_test,
                "Interactivity Test": interact_test,
                "Click Test": click_test,
                "code_snippet": button_html
            }

        results[form_description] = {
            **form_results,
            "code_snippet": form_html
        }

    return results


# Test data for data-driven testing and boundary testing
test_data = {
    "text": ["", "a" * 10, "a" * 255, "special@#$%^&*()"],
    "password": ["", "a" * 10, "a" * 255, "special@#$%^&*()"],
    "email": ["", "test@example.com", "invalid-email", "a" * 245 + "@example.com"],
    "number": ["", "123", "-123", "abc", "12345678901234567890"],
    "textarea": ["", "a" * 10, "a" * 1024, "special@#$%^&*()"]
}


def test_input_fields(form):
    """Test input fields within a form using data-driven tests and boundary testing."""
    results = {}
    inputs = form.find_elements(By.CSS_SELECTOR, "input, textarea")
    for input in inputs:
        input_type = input.get_attribute("type") or input.tag_name
        input_name = input.get_attribute("name") or "Unnamed Input"

        if input_type in ["text", "password", "email", "textarea", "number"]:
            for value in test_data.get(input_type, ["test"]):  # Use default ["test"] if input_type is not in test_data
                test_description = f"{input.tag_name} {input_type} {input_name} with tested value (length {len(value)})"
                test_result = "passed - Filled or Checked"

                try:
                    input.clear()  # Clear the input field before each test

                    if input_type in ["text", "password", "email", "textarea"]:
                        input.send_keys(value)
                    elif input_type == "number":
                        input.send_keys(value)
                        entered_value = input.get_attribute("value")

                        if not value.isnumeric() and entered_value != "":
                            test_result = f"failed - Numeric input accepted non-numeric value:\n'{value}'"
                        elif value.isnumeric() and entered_value != value:
                            test_result = f"failed - Numeric input did not accept valid number:\n'{value}'"

                except ElementNotInteractableException:
                    test_result = f"failed - Element not intractable tested value (length {len(value)})"
                except TimeoutException:
                    test_result = "failed - TimeoutException"
                except StaleElementReferenceException:
                    test_result = "failed - StaleElementReferenceException"
                except Exception as e:
                    test_result = f"failed - Exception: {str(e)}"

                results[test_description] = test_result

        elif input_type in ["checkbox", "radio"]:
            test_description = f"{input.tag_name} {input_type} {input_name}"
            test_result = "passed - Clicked or Checked"
            try:
                input.click() if not input.is_selected() else None
            except Exception as e:
                test_result = f"failed - Exception: {str(e)}"
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
        pass
    except Exception as e:
        results[test_description] = f"failed - Exception: {str(e)}"
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
