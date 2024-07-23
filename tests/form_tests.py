from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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
        results[form_description] = {
            **test_input_fields(form),
            **test_form_submission(form, driver),
            "code_snippet": form_html
        }
    return results


# Test data for data-driven testing and boundary testing
test_data = {
    "text": ["", "a" * 10, "a" * 255, "special@#$%^&*()"],
    "password": ["", "a" * 10, "a" * 255, "special@#$%^&*()"],
    "email": ["", "test@example.com", "invalid-email", "a" * 245 + "@example.com"],
    "number": ["", "123", "-123", "abc", "12345678901234567890"],
    "textarea": ["", "a" * 10, "a" * 1024, "special@#$%^&*()"],
    "date": ["", "2024-07-23", "23-07-2024", "invalid-date"],
    "tel": ["", "+1234567890", "123-456-7890", "invalid-phone"],
}

test_data['card'] = test_data['number']


def test_input_fields(form):
    """Test input fields within a form using data-driven tests and boundary testing."""
    results = {}
    forms_elements = form.find_elements(By.CSS_SELECTOR, "input, textarea, select")

    for input in forms_elements:
        input_type = input.get_attribute("type") or input.tag_name
        input_name = input.get_attribute("name") or "Unnamed Input"

        # Custom checks for specific input names
        if input_name.lower() in ["email", "mail"] and input_type != "email":
            results[
                f"{input.tag_name} {input_name}"] = "Failed - Input type should be 'email' but currently accepts invalid email inputs"
            continue
        if input_name.lower() in ["card", "credit card", "phone number"] and input_type != "number":
            results[
                f"{input.tag_name} {input_name}"] = "Failed - Input type should be 'number' but currently accepts non-numeric inputs"
            continue
        if input_name.lower() in ["birthdate", "date"] and input_type != "date":
            results[
                f"{input.tag_name} {input_name}"] = "Failed - Input type should be 'date' but currently accepts non-date values"
            continue
        if input_name.lower() in ["phone", "telephone"] and input_type != "tel":
            results[
                f"{input.tag_name} {input_name}"] = "Failed - Input type should be 'tel' but currently accepts non-telephone values"
            continue
        if input_name.lower() in ["confirm_password"] and input_type != "password":
            results[
                f"{input.tag_name} {input_name}"] = "Failed - Input type should be 'password' but currently accepts non-password values"
            continue

        elif input_type in ["text", "password", "email", "textarea", "number", "url", "date", "tel"]:
            for value in test_data.get(input_type, ["test"]):  # Use default ["test"] if input_type is not in test_data
                test_description = f"{input.tag_name} {input_type} {input_name} with tested value (length {len(value)})"
                test_result = "passed - Filled or Checked"

                try:
                    input.clear()  # Clear the input field before each test

                    if input_type in ["text", "password", "email", "textarea", "url", "date", "tel"]:
                        input.send_keys(value)
                    elif input_type == "number":
                        input.send_keys(value)
                        entered_value = input.get_attribute("value")

                        if not value.isnumeric() and entered_value != "":
                            test_result = f"Failed - Numeric input accepted non-numeric value:\n'{value}'"
                        elif value.isnumeric() and entered_value != value:
                            test_result = f"Failed - Numeric input did not accept valid number:\n'{value}'"

                except ElementNotInteractableException:
                    test_result = f"Failed - Element not intractable tested value (length {len(value)})"
                except TimeoutException:
                    test_result = "Failed - TimeoutException"
                except StaleElementReferenceException:
                    test_result = "Failed - StaleElementReferenceException"
                except Exception as e:
                    test_result = f"Failed - Exception: {str(e)}"

                results[test_description] = test_result

        elif input_type in ["checkbox", "radio"]:
            test_description = f"{input.tag_name} {input_type} {input_name}"
            test_result = "passed - Clicked or Checked"
            try:
                input.click() if not input.is_selected() else None
            except Exception as e:
                test_result = f"Failed - Exception: {str(e)}"
            results[test_description] = test_result

        elif input.tag_name == "select":
            test_description = f"{input.tag_name} {input_name}"
            test_result = "passed - Options Selected"
            try:
                select = Select(input)
                for option in select.options:
                    select_val = option.get_attribute("value")
                    if select_val == '' or select_val is None:
                        test_result = f"Failed - Select option: ({option.text}) - does not match a value property)"
                    else:
                        if option.is_enabled() and select_val.lower() == option.text.lower():
                            select.select_by_value(select_val)
                        elif not option.is_enabled():
                            test_result = f"Failed - Select element not enabled for option {option.text}"
                        elif not input.is_displayed():
                            test_result = f"Failed - Select element not displayed for option {option.text}"
            except Exception as e:
                test_result = f"Failed - Exception: {str(e)}"
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
