from urllib.parse import urlparse
from playwright.sync_api import sync_playwright


def buttons_url_test(page_url):
    """
    Loads the url and extract all the buttons.
    checks if all the buttons are loaded, visible and when are click does not lead to failure.
    :param page_url: url of the page
    :return: dict of test results.
    """
    # Use a more stable selector if possible, and wait for the general presence of buttons
    page_url.wait_for_selector("button", state="visible", timeout=50000)
    buttons = page_url.query_selector_all("button")
    return btns_test(page_url, buttons, False)


def buttons_code_test(page):
    """
    Extract all the buttons from the HTML code.
    checks if all the buttons are loaded, visible and when are click does not lead to failure.
    :param page: HTML code.
    :return: dict of test results.
    """
    buttons = page.query_selector_all("button")
    return btns_test(page, buttons, False)


def btns_test(page, buttons, is_url=True):
    """
    Tests buttons for visibility, text content, and intractability.
    :return: List of dictionaries with results for each button test.
    """
    results = []
    for index, button in enumerate(buttons):
        button_text = button.text_content()
        if button_text:
            button_text = button_text.strip()

        test_name = f"Test for Button {index + 1}"
        result = {
            "name": test_name,
            "button_text": button_text,
            "outcome": ""
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
        results = buttons_url_test(page)
        browser.close()
        return results, filename
