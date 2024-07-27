from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    all_a_tags = soup.find_all("a")
    links = []
    for tag in all_a_tags:
        href = tag.get('href', 'no-href-attribute')
        if href == "":
            href = "empty-href-attribute"
        links.append((href, str(tag)))
    return links


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
    test_name = "Check Broken Link"
    # Skip internal page links and mailto links
    if link.startswith("#") or link.startswith("mailto:"):
        return test_name, "passed"
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
        return test_name, "failed - Invalid Request"
    except Exception:
        return test_name, "failed - Failed to run test"


def check_incorrect_url(link):
    test_name = "Check Valid URL Format"
    # Check for valid URL, mailto link, or internal link
    parsed_url = urlparse(link)
    if link.startswith('#') or link.startswith("mailto:") or (
            parsed_url.scheme in ['http', 'https'] and parsed_url.netloc):
        return test_name, "passed"
    else:
        return test_name, "failed - URL does not start with 'http', 'https', or 'mailto'"


def check_non_responsive_link(link):
    test_name = "Check Responsive Link"
    # Skip internal page links and mailto links
    if link.startswith("#") or link.startswith("mailto:"):
        return test_name, "passed"
    try:
        response = requests.get(link, timeout=5)
        if response.status_code == 200 and len(response.content) > 0:
            return test_name, "passed"
        else:
            return test_name, f"failed - Status Code: {response.status_code}"
    except requests.RequestException:
        return test_name, f"failed - Failed to run test"


def check_invalid_destination(link):
    test_name = "Check Invalid Destination"
    # Skip internal page links and mailto links
    if link.startswith("#") or link.startswith("mailto:"):
        return test_name, "passed"
    try:
        response = requests.get(link, timeout=5)
        if response.status_code == 404:
            return test_name, "failed - Page not found (404)"
        else:
            return test_name, "passed"
    except requests.exceptions.ConnectionError:
        return test_name, "failed - Unable to connect"
    except requests.RequestException:
        return test_name, "failed - Failed to run test"


def run_tests_on_links(links):
    results = {}
    for link, link_html in links:
        results[link] = {
            "code_snippet": link_html
        }
        for check in [check_broken_link, check_incorrect_url, check_non_responsive_link, check_invalid_destination]:
            test_name, result = check(link)
            results[link][test_name] = result
    return results


def execute_url_tests(url):
    all_links = extract_links_from_page(url)
    results = run_tests_on_links(all_links)
    return results


def execute_html_tests(html_content):
    links = extract_links_from_html(html_content)
    results = run_tests_on_links(links)
    return results
