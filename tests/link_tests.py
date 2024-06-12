from urllib.parse import urlparse
from playwright.async_api import async_playwright
import requests

link_test_descriptions = {
    "links_url_test": "Loads the URL and extracts all the links. Checks if all the links are loaded, visible, and when clicked do not lead to failure.",
    "links_code_test": "Extracts all the links from the HTML code. Checks if all the links are loaded, visible, and when clicked do not lead to failure.",
    "check_visibility": "Checks if the link is visible.",
    "check_href": "Checks if the link has a valid href attribute.",
    "check_interactive": "Checks if the link is interactable.",
    "check_broken_links": "Checks if the link is broken (404 error).",
    "check_anchor": "Checks if the link points to a valid anchor within the page.",
    "check_javascript_link": "Checks if the link uses JavaScript and does not provide a meaningful action."
}


def get_link_test_description(method_name):
    """
    Returns the test description associated with the given method name.
    :param method_name: Name of the test method.
    :return: Description of the test method.
    """
    return link_test_descriptions.get(method_name, "Test description not found.")


async def links_url_test(page):
    """
    Loads the URL and extracts all the links.
    Checks if all the links are loaded, visible, and when clicked do not lead to failure.
    :param page: Playwright page object
    :return: List of test results.
    """
    await page.wait_for_selector("a", state="visible", timeout=50000)
    links = await page.query_selector_all("a")
    return await links_test(links, "links_url_test", page)


async def links_code_test(page):
    """
    Extracts all the links from the HTML code.
    Checks if all the links are loaded, visible, and when clicked do not lead to failure.
    :param page: Playwright page object
    :return: List of test results.
    """
    links = await page.query_selector_all("a")
    return await links_test(links, "links_code_test", page)


async def check_visibility(link):
    """
    Checks if the link is visible.
    :param link: Link element.
    :return: "PASSED" or "FAILED" with the reason.
    """
    if await link.is_visible():
        return "PASSED - Link is visible."
    else:
        return "FAILED - Link is not visible."


async def check_href(link):
    """
    Checks if the link has a valid href attribute.
    :param link: Link element.
    :return: "PASSED" or "FAILED" with the reason.
    """
    link_href = await link.get_attribute("href")
    if link_href:
        return "PASSED - Link has href attribute.", link_href
    else:
        return "FAILED - No href attribute.", None


async def check_interactive(link):
    """
    Checks if the link is interactable.
    :param link: Link element.
    :return: "PASSED" or "FAILED" with the reason.
    """
    if await link.is_enabled():
        return "PASSED - Link is interactable."
    else:
        return "FAILED - Link is not interactable."


async def check_broken_link(link_href):
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


async def check_anchor(link_href, page):
    """
    Checks if the link points to a valid anchor within the page.
    :param link_href: Href attribute of the link.
    :param page: Playwright page object
    :return: "PASSED" or "FAILED" with the reason.
    """
    if link_href.startswith("#"):
        anchor_id = link_href[1:]
        try:
            if await page.query_selector(f"#{anchor_id}"):
                return "PASSED - Valid anchor."
            else:
                return "FAILED - Invalid anchor."
        except Exception as e:
            return f"FAILED - Error checking anchor: {str(e)}"
    return "SKIPPED - Not an anchor link."


async def check_javascript_link(link_href):
    """
    Checks if the link uses JavaScript and does not provide a meaningful action.
    :param link_href: Href attribute of the link.
    :return: "PASSED" or "FAILED" with the reason.
    """
    if link_href.startswith("javascript:"):
        return "FAILED - Link uses JavaScript."
    return "SKIPPED - Not a JavaScript link."


async def links_test(links, test_name, page):
    """
    Tests links for visibility, href content, intractability, and checks for broken links.
    :param links: List of link elements.
    :param test_name: Name of the test method.
    :param page: Playwright page object
    :return: List of dictionaries with results for each link test.
    """
    results = []

    # Extract link details before interaction
    link_details = []
    for link in links:
        link_text = await link.text_content()
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
        result["outcomes"]["Visibility Test"] = await check_visibility(link)

        # Test for href attribute
        href_outcome, link_href = await check_href(link)
        result["outcomes"]["Href Test"] = href_outcome
        result["link_href"] = link_href

        if link_href:
            # Test for interactivity
            result["outcomes"]["Interactivity Test"] = await check_interactive(link)

            # Test for broken link
            result["outcomes"]["Broken Link Test"] = await check_broken_link(link_href)

            # Test for anchor link
            result["outcomes"]["Anchor Link Test"] = await check_anchor(link_href, page)

            # Test for JavaScript link
            result["outcomes"]["JavaScript Link Test"] = await check_javascript_link(link_href)
        else:
            result["outcomes"]["Interactivity Test"] = "FAILED - No href to test."
            result["outcomes"]["Broken Link Test"] = "FAILED - No href to test."
            result["outcomes"]["Anchor Link Test"] = "FAILED - No href to test."
            result["outcomes"]["JavaScript Link Test"] = "FAILED - No href to test."

        # Determine overall outcome
        if all(outcome.startswith("PASSED") for outcome in result["outcomes"].values() if outcome != "SKIPPED"):
            result["overall_outcome"] = "PASSED - All tests passed successfully."
        else:
            failed_tests = [test for test, outcome in result["outcomes"].items() if outcome.startswith("FAILED")]
            result["overall_outcome"] = f"FAILED - {', '.join(failed_tests)}."

        results.append(result)
    return results


async def run_link_tests_html_code(html_content):
    """
    Runs all the tests for an HTML code.
    :param html_content: HTML content of the page.
    :return: Results of the link tests and the filename.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html_content)
        title = await page.title() or "test_page"
        filename = f"./results/{title}_link_tests.txt"
        results = await links_code_test(page)
        await browser.close()
        return results, filename


async def run_url_link_tests(url):
    """
    Runs the tests for a given URL.
    :param url: URL of the page.
    :return: Results of the link tests and the filename.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.replace("www.", "")
        filename = f"./results/{domain_name}_link_tests.txt"
        results = await links_url_test(page)
        await browser.close()
        return results, filename

