import os
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse


def buttons_url_test(page_url):
    """
    Loads the url and extract all the buttons.
    checks if all the buttons are loaded, visible and when are click does not lead to failure.
    :param page_url: url of the page
    :return: dict of test results.
    """
    # Use a more stable selector if possible, and wait for the general presence of buttons
    page_url.wait_for_selector("button", state="visible", timeout=50000)  # Increased timeout

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


def run_tests_html_code(html_content, output_dir='./websitesTestsResult'):
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
        filename = os.path.join(output_dir, f"{title}_button_tests.txt")
        os.makedirs(output_dir, exist_ok=True)

        # Get test results
        results = buttons_code_test(page)
        browser.close()
        write_results_to_file(results, filename)


def run_tests_url(url, output_dir='./websitesTestsResult'):
    """
    Runs the tests for a given URL.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the URL directly
        page.goto(url, wait_until="networkidle")

        # Generate a simple filename from the domain name of the URL
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.replace("www.", "")  # Removes 'www.' if present
        filename = os.path.join(output_dir, f"{domain_name}_button_tests.txt")
        os.makedirs(output_dir, exist_ok=True)

        # Get test results
        results = buttons_url_test(page)
        browser.close()
        write_results_to_file(results, filename)


def run_tests_wrapper(web_data, output_dir='./websitesTestsResult'):
    """
    Wrapper function for run_tests, if the website is an HTML code or a URL.
    Writes the results into a file.
    :param web_data: HTML code or URL.
    """
    if web_data.startswith("http"):
        run_tests_url(web_data, output_dir)
    else:
        run_tests_html_code(web_data, output_dir)


def get_html_content(file_path):
    """Reads an HTML file from the given path and returns its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def write_results_to_file(results, filename):
    """Writes the test results to a file."""
    with open(filename, "w") as file:
        for result in results:
            file.write(f"### {result['name']} ###\n")
            file.write(f"Button Text: {result['button_text']}\n")
            file.write(f"Result: {result['outcome']}\n\n")


def test_html_file(file_path, output_dir='./websitesTestsResult'):
    """
    Tests an HTML file given its path.
    """
    html_content = get_html_content(file_path)
    if html_content:
        run_tests_html_code(html_content, output_dir)


def test_url(url, output_dir='./websitesTestsResult'):
    """
    Tests a URL by first retrieving its HTML content and then calling the HTML test method.
    """
    run_tests_url(url, output_dir)


if __name__ == "__main__":
    # Example usage:
    html_file_path = '../Websites_Generator/generated_html/buggy_website.html'  # Replace this with the actual file path
    url_to_test = 'https://themeforest.net/search/dummy'  # URL to test

    test_html_file(html_file_path)
    test_url(url_to_test)
