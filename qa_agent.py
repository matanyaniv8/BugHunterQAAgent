import tests.link_tests
from urllib.parse import urlparse


def run_tests_wrapper(web_data):
    """
    Wrapper function for running tests on buttons, links, and forms.
    Writes the results into a single file.
    :param web_data: HTML code or URL.
    """
    is_url = web_data.startswith("http")
    if is_url:
        return tests.link_tests.execute_url_tests(web_data)
    else:
        return tests.link_tests.execute_html_tests(web_data)


def get_html_content(file_path):
    """
    Reads an HTML file from the given path and returns its content.
    :param file_path: Path to the HTML file.
    :return: Content of the HTML file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def get_domain_from_url(url):
    """
    Extracts the domain name from a URL.
    :param url: URL to extract the domain from.
    :return: Domain name.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def execute_html_tests(file_path):
    """
    Runs the tests on the given HTML file and returns the results filepath.
    :param file_path: Path to the HTML file.
    :return: Path to the results file.
    """
    html_content = get_html_content(file_path)
    if html_content:
        return run_tests_wrapper(html_content)

    return None


def execute_url_tests(url):
    """
    Runs the tests on the given URL and returns the results filepath.
    :param url: URL to run the tests on.
    :return: Path to the results file.
    """
    return run_tests_wrapper(url)
