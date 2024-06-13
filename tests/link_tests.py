import requests
from bs4 import BeautifulSoup
from requests_html import HTML


def extract_links_from_html(html_content):
    html = HTML(html=html_content)
    return list(html.absolute_links)


def extract_links_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags
        links = soup.find_all('a')

        # Extract the href attribute from each <a> tag
        urls = [link.get('href') for link in links if link.get('href') is not None]

        return urls
    else:
        return []


def check_broken_link(link):
    test_name = "check_broken_link"
    try:
        response = requests.head(link, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return test_name, "passed"
        else:
            return test_name, f"failed - Status Code: {response.status_code}"
    except requests.RequestException as e:
        return test_name, f"failed - Exception: {e}"


def check_incorrect_url(link):
    test_name = "check_incorrect_url"
    try:
        # Basic validation: URL should start with 'http' or 'https'
        if link.startswith('http'):
            return test_name, "passed"
        else:
            return test_name, "failed - URL does not start with 'http' or 'https'"
    except Exception as e:
        return test_name, f"failed - Exception: {e}"


def check_non_responsive_link(link):
    test_name = "check_non_responsive_link"
    try:
        response = requests.get(link, timeout=5)
        if response.status_code == 200 and len(response.content) > 0:
            return test_name, "passed"
        else:
            return test_name, f"failed - Status Code: {response.status_code}, Content Length: {len(response.content)}"
    except requests.RequestException as e:
        return test_name, f"failed - Exception: {e}"


def run_tests_on_links(links):
    results = {}
    for link in links:
        results[link] = {}
        for check in [check_broken_link, check_incorrect_url, check_non_responsive_link]:
            test_name, result = check(link)
            results[link][test_name] = result
    return results


def execute_url_tests(url):
    print(f"Start running test on {url}")
    all_links = extract_links_from_page(url)
    print(f"extracted all link - total of {len(all_links)} links")
    results = run_tests_on_links(all_links[:3])
    return results


def execute_html_tests(html_content):
    print(f"Start running test on html")
    links = extract_links_from_html(html_content)
    results = run_tests_on_links(links)
    return results
