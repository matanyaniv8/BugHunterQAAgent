from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import requests

link_test_descriptions = {
    "links_url_test": "Loads the URL and extracts all the links. Checks if all the links are loaded, visible, and when clicked do not lead to failure.",
    "links_code_test": "Extracts all the links from the HTML code. Checks if all the links are loaded, visible, and when clicked do not lead to failure.",
    "check_visibility": "Checks if the link is visible.",
    "check_href": "Checks if the link has a valid href attribute.",
    "check_interactive": "Checks if the link is intractable.",
    "check_broken_links": "Checks if the link is broken (404 error)."
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
    return links_test(page_url, links)


def links_code_test(page):
    """
    Extracts all the links from the HTML code.
    Checks if all the links are loaded, visible, and when clicked do not lead to failure.
    :param page: HTML code.
    :return: dict of test results.
    """
    links = page.query_selector_all("a")
    return links_test(page, links)


def check_visibility(link):
    """
    Checks if the link is visible.
    :param link: Link element.
    :return: "PASSED" or "FAILED" with the reason.
    """
    if link.is_visible():
        return "PASSED - Link is visible."
    else:
        return "FAILED - Link is not visible."


def check_href(link):
    """
    Checks if the link has a valid href attribute.
    :param link: Link element.
    :return: "PASSED" or "FAILED" with the reason.
    """
    link_href = link.get_attribute("href")
    if link_href:
        return "PASSED - Link has href attribute.", link_href
    else:
        return "FAILED - No href attribute.", None


def check_interactive(link):
    """
    Checks if the link is interactable.
    :param link: Link element.
    :return: "PASSED" or "FAILED" with the reason.
    """
    if link.is_enabled():
        return "PASSED - Link is interactable."
    else:
        return "FAILED - Link is not interactable."


def check_broken_link(link_href):
    """
    Checks if the link is broken (404 error).
    :param link_href: Href attribute of the link.
    :return: "PASSED" or "FAILED" with the reason.
    """
    if not link_href.startswith("http"):
        return f"FAILED - Invalid URL '{link_href}': No scheme supplied. Perhaps you meant http://{link_href}?"

    try:
        response = requests.get(link_href)
        if response.status_code == 404:
            return "FAILED - 404 error."
        else:
            return "PASSED - Link is valid."
    except requests.RequestException as e:
        return f"FAILED - Request error: {str(e)}"


def links_test(links, test_name):
    """
    Tests links for visibility, href content, interactability, and checks for broken links.
    :return: List of dictionaries with results for each link test.
    """
    results = []

    # Extract link details before interaction
    link_details = []
    for link in links:
        link_text = link.text_content()
        if link_text:
            link_text = link_text.strip()

        link_details.append((link, link_text))

    for index, (link, link_text) in enumerate(link_details):
        individual_test_name = f"Test for Link {index + 1}"
        result = {
            "name": individual_test_name,
            "link_text": link_text,
            "link_href": "",
            "outcomes": {},
            "overall_outcome": "",
            "test_description": get_link_test_description(test_name)
        }

        # Test for visibility
        result["outcomes"]["Visibility Test"] = check_visibility(link)

        # Test for href attribute
        href_outcome, link_href = check_href(link)
        result["outcomes"]["Href Test"] = href_outcome
        result["link_href"] = link_href

        if link_href:
            # Test for interactivity
            result["outcomes"]["Interactivity Test"] = check_interactive(link)

            # Test for broken link
            result["outcomes"]["Broken Link Test"] = check_broken_link(link_href)
        else:
            result["outcomes"]["Interactivity Test"] = "FAILED - No href to test."
            result["outcomes"]["Broken Link Test"] = "FAILED - No href to test."

        # Determine overall outcome
        if all(outcome.startswith("PASSED") for outcome in result["outcomes"].values()):
            result["overall_outcome"] = "PASSED - All tests passed successfully."
        else:
            failed_tests = [test for test, outcome in result["outcomes"].items() if outcome.startswith("FAILED")]
            result["overall_outcome"] = f"FAILED - {', '.join(failed_tests)}."

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
