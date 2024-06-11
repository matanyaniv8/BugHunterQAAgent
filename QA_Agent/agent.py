from playwright.sync_api import sync_playwright
from urllib.parse import urlparse


def test_buttons_url(page_url):
    """
    Loads the url and extract all the buttons.
    checks if all the buttons are loaded, visible and when are click does not lead to failure.
    :param page_url: url of the page
    :return: dict of test results.
    """
    # Use a more stable selector if possible, and wait for the general presence of buttons
    page_url.wait_for_selector("button", state="visible", timeout=50000)  # Increased timeout

    buttons = page_url.query_selector_all("button")
    buttons = page_url.query_selector_all("button")

    return test_btns(page_url, buttons, False)


def test_buttons_code(page):
    """
    Extract all the buttons from the HTML code.
    checks if all the buttons are loaded, visible and when are click does not lead to failure.
    :param page: HTML code.
    :return: dict of test results.
    """
    buttons = page.query_selector_all("button")
    return test_btns(page, buttons, False)


def test_btns(page, buttons, is_url=True):
    """
    Tests buttons for visibility, text content, and intractability.
    :return: List of dictionaries with results for each button test.
    """
    results = []
    for index, button in enumerate(buttons):
        # Check each button's text content
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
                # Ensure the button is interactable before attempting to click
                if button.is_visible() and button.is_enabled():
                    button.click()
                    if is_url:
                        page.wait_for_timeout(500)  # Adjust timing as necessary
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
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        # Set the HTML content directly
        page.set_content(html_content)

        # Generate a simple filename from a title or default to 'test_page'
        title = page.title() or "test_page"
        filename = f"./websitesTestsResult/{title}_button_tests.txt"

        # Get test results
        results = test_buttons_code(page)
        browser.close()
        return results, filename


def run_url_tests(url):
    """
    Runs the tests for a given url.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the URL directly
        page.goto(url, wait_until="networkidle")

        # Generate a simple filename from the domain name of the URL
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.replace("www.", "")  # Removes 'www.' if present
        filename = f"./websitesTestsResult/{domain_name}_button_tests.txt"

        # Get test results
        results = test_buttons_url(page)

        browser.close()
        return results, filename


def run_tests_wrapper(web_data):
    """
    Wrapper function for run_tests, if the website is an HTML code or an url.
    writes the results into a file.
    :param web_data: HTML code or url.
    """
    if web_data.startswith("http"):
        results, filename = run_url_tests(web_data)
    else:
        results, filename = run_tests_html_code(web_data)

    # Write results to a file
    with open(filename, "w") as file:
        for result in results:
            file.write(f"### {result['name']} ###\n")
            file.write(f"Button Text: {result['button_text']}\n")
            file.write(f"Result: {result['outcome']}\n\n")


def get_html_content(file_path):
    """Reads an HTML file from the given path and returns its content."""
    file_content = None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return file_content


if __name__ == "__main__":
    web_path = 'testPage.html'  # Replace this with the actual file path
    html_content = get_html_content(web_path)
    run_tests_wrapper(html_content)
    url = 'https://themeforest.net/search/dummy'  # URL to test
    run_tests_wrapper(url)
