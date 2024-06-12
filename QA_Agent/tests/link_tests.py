from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

link_test_descriptions = {
    "links_url_test": "Loads the URL and extracts all the links. Checks if all the links are loaded, visible, and when clicked do not lead to failure.",
    "links_code_test": "Extracts all the links from the HTML code. Checks if all the links are loaded, visible, and when clicked do not lead to failure.",
    "links_test": "Tests links for visibility, href content, and interactability."
}


def get_link_test_description(method_name):
    """
    Returns the test description associated with the given method name.
    :param method_name: Name of the test method.
    :return: Description of the test method.
    """
    return link_test_descriptions.get(method_name, "Test description not found.")


def links_url_test(page_url):
    """
    Loads the URL and extracts all the links.
    Checks if all the links are loaded, visible, and when clicked do not lead to failure.
    :param page_url: URL of the page
    :return: dict of test results.
    """
    page_url.wait_for_selector("a", state="visible", timeout=50000)
    links = page_url.query_selector_all("a")
    return links_test(page_url, links, False, "links_url_test")


def links_code_test(page):
    """
    Extracts all the links from the HTML code.
    Checks if all the links are loaded, visible, and when clicked do not lead to failure.
    :param page: HTML code.
    :return: dict of test results.
    """
    links = page.query_selector_all("a")
    return links_test(page, links, False, "links_code_test")


def links_test(page, links, is_url, test_name):
    """
    Tests links for visibility, href content, and interactability.
    :return: List of dictionaries with results for each link test.
    """
    results = []

    # Extract link details before interaction
    link_details = []
    for link in links:
        link_text = link.text_content()
        if link_text:
            link_text = link_text.strip()

        link_href = link.get_attribute("href")
        link_details.append((link, link_text, link_href))

    for index, (link, link_text, link_href) in enumerate(link_details):
        individual_test_name = f"Test for Link {index + 1}"
        result = {
            "name": individual_test_name,
            "link_text": link_text,
            "link_href": link_href,
            "outcome": "",
            "test_method": test_name,
            "test_description": get_link_test_description(test_name)
        }

        if not link_href:
            result["outcome"] = "FAILED - No href attribute."
        else:
            try:
                if link.is_visible() and link.is_enabled():
                    result["outcome"] = "PASSED - Link has href and is interactable."
                    if is_url:
                        with page.expect_navigation():
                            link.click()
                    else:
                        link.click()
                else:
                    result["outcome"] = "FAILED - Link is not interactable."
            except Exception as e:
                result["outcome"] = f"FAILED - Error during clicking: {str(e)}"

        results.append(result)
    return results


def run_link_tests_html_code(html_content):
    """
    Runs all the tests for an HTML code.

    :param html_content: HTML content of the page.
    :return: Results of the link tests and the filename.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        title = page.title() or "test_page"
        filename = f"./websitesTestsResult/{title}_link_tests.txt"
        results = links_code_test(page)
        browser.close()
        return results, filename


def run_url_link_tests(url):
    """
    Runs the tests for a given URL.
    :param url: URL of the page.
    :return: Results of the link tests and the filename.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.replace("www.", "")
        filename = f"./websitesTestsResult/{domain_name}_link_tests.txt"
        results = links_url_test(page)
        browser.close()
        return results, filename

