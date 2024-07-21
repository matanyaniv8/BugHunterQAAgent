from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from requests_html import HTML


def extract_links_from_html(html_content):
    html = HTML(html=html_content)
    return list(html.absolute_links)


def extract_links_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        # Ensure all URLs are absolute by combining the base URL with the relative URL
        urls = [(urljoin(url, link.get('href')), str(link)) for link in links if link.get('href') is not None]
        return urls
    else:
        return []


def check_broken_link(link):
    test_name = "check broken link"
    try:
        response = requests.head(link, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return test_name, "passed"
        else:
            return test_name, f"failed - Status Code: {response.status_code}"
    except requests.exceptions.InvalidURL:
        return test_name, "failed - Invalid URL format"
    except requests.exceptions.ConnectionError:
        return test_name, "failed - Unable to connect"
    except requests.RequestException:
        return test_name, f"failed - Invalid Request"
    except Exception:
        return test_name, "failed - Failed to run test"


def check_incorrect_url(link):
    test_name = "Check valid URL format"
    if link.startswith('http'):
        return test_name, "passed"
    else:
        return test_name, "failed - URL does not start with 'http' or 'https'"


def check_non_responsive_link(link):
    test_name = "check responsive link"
    try:
        response = requests.get(link, timeout=5)
        if response.status_code == 200 and len(response.content) > 0:
            return test_name, "passed"
        else:
            return test_name, f"failed - Status Code: {response.status_code}"
    except requests.RequestException:
        return test_name, f"failed - Failed to run test"


def run_tests_on_links(links):
    results = {}
    for link, link_html in links:
        results[link] = {
            "code_snippet": link_html
        }
        for check in [check_broken_link, check_incorrect_url, check_non_responsive_link]:
            test_name, result = check(link)
            results[link][test_name] = result
    return results


def execute_url_tests(url):
    print(f"Start running test on {url}")
    all_links = extract_links_from_page(url)
    print(f"Extracted all links - total of {len(all_links)} links")
    results = run_tests_on_links(all_links)
    return results


def execute_html_tests(html_content):
    print(f"Start running test on HTML content")
    links = extract_links_from_html(html_content)
    link_htmls = [(link, "") for link in links]  # No HTML available for these links
    results = run_tests_on_links(link_htmls)
    return results
