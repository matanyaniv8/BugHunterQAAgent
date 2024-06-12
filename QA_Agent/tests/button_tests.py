from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

# Dictionary to map method names to their descriptions
test_descriptions = {
    "buttons_url_test": "Loads the URL and extracts all the buttons. Checks if all the buttons are loaded, visible, and when clicked do not lead to failure.",
    "buttons_code_test": "Extracts all the buttons from the HTML code. Checks if all the buttons are loaded, visible, and when clicked do not lead to failure.",
    "btns_test": "Tests buttons for visibility, text content, and interactability."
}


def get_test_description(method_name):
    """
    Returns the test description associated with the given method name.
    :param method_name: Name of the test method.
    :return: Description of the test method.
    """
    return test_descriptions.get(method_name, "Test description not found.")


def buttons_url_test(page_url):
    """
    Loads the URL and extracts all the buttons.
    Checks if all the buttons are loaded, visible, and when clicked do not lead to failure.
    :param page_url: URL of the page
    :return: dict of test results.
    """
    page_url.wait_for_selector("button", state="visible", timeout=50000)
    buttons = page_url.query_selector_all("button")
    return btns_test(page_url, buttons, False, "buttons_url_test")


def buttons_code_test(page):
    """
    Extracts all the buttons from the HTML code.
    Checks if all the buttons are loaded, visible, and when clicked do not lead to failure.
    :param page: HTML code.
    :return: dict of test results.
    """
    buttons = page.query_selector_all("button")
    return btns_test(page, buttons, False, "buttons_code_test")


def btns_test(page, buttons, is_url, test_name):
    """
    Tests buttons for visibility, text content, and interactability.
    :return: List of dictionaries with results for each button test.
    """
    results = []
    for index, button in enumerate(buttons):
        button_text = button.text_content()
        if button_text:
            button_text = button_text.strip()

        individual_test_name = f"Test for Button {index + 1}"
        result = {
            "name": individual_test_name,
            "button_text": button_text,
            "outcome": "",
            "test_method": test_name,
            "test_description": get_test_description(test_name)
        }

        if not button_text:
            result["outcome"] = "FAILED - No visible text."
        else:
            try:
                if button.is_visible() and button.is_enabled():
                    button.click()
                    if is_url:
                        page.wait_for_timeout(500)
                    result["outcome"] = "PASSED - Button has text and no errors after clicking."
                else:
                    result["outcome"] = "FAILED - Button is not interactable."
            except Exception as e:
                result["outcome"] = f"FAILED - Error during clicking: {str(e)}"

        results.append(result)
    return results


def run_tests_html_code(html_content):
    """
    Runs all the tests for an HTML code.

    :param html_content: HTML content of the page.
    :return: Results of the button tests and the filename.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        title = page.title() or "test_page"
        filename = f"./websitesTestsResult/{title}_button_tests.txt"
        results = buttons_code_test(page)
        browser.close()
        return results, filename


def run_url_tests(url):
    """
    Runs the tests for a given URL.
    :param url: URL of the page.
    :return: Results of the button tests and the filename.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.replace("www.", "")
        filename = f"./websitesTestsResult/{domain_name}_button_tests.txt"
        try:
            results = buttons_url_test(page)
            browser.close()
            return results, filename
        except Exception as e:
            browser.close()
            return {}, filename
