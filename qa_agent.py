import tests.link_tests as link_tests
import tests.button_tests as button_tests
from urllib.parse import urlparse
from tests import form_tests
from w3c_validator import validate


def run_tests_wrapper(web_data):
    """
    Wrapper function for running tests on buttons, links, and forms.
    Writes the results into a single file.
    :param web_data: HTML code or URL.
    """
    is_url = web_data.startswith("http")
    if is_url:
        link_results = link_tests.execute_url_tests(web_data)
        button_results = button_tests.execute_forms_url_tests(web_data)
        form_results = form_tests.execute_forms_url_tests(web_data)
    else:
        link_results = link_tests.execute_html_tests(web_data)
        button_results = button_tests.execute_forms_html_tests(web_data)
        form_results = form_tests.execute_forms_html_tests(web_data)

    unified_results = {
        "links": link_results,
        "buttons": button_results,
        "forms": form_results
    }
    print(unified_results)
    return unified_results


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
    validate_html_or_url(file_path)
    html_content = get_html_content(file_path)
    unified_results = None
    if html_content:
        unified_results = run_tests_wrapper(html_content)
        unified_results['W3C Validation Report'] = validate_html_or_url(file_path)
    return unified_results


def execute_url_tests(url):
    """
    Runs the tests on the given URL and returns the results filepath.
    :param url: URL to run the tests on.
    :return: Path to the results file.
    """
    results = run_tests_wrapper(url)

    results['W3C Validation Report'] = validate_html_or_url(url)

    return results


def validate_html_or_url(url_or_file):
    """"
    Validate the HTML content from a URL or file
    :param url_or_file: URL or file to validate.
    :return: Validated Test Results."""
    result = validate(url_or_file)
    results = {}
    for i in result['messages']:
        message_type = i['type']

        message_type = 'Warning' if message_type == 'info' else message_type
        desc = f"{message_type} in Line {i['lastLine']}"
        results[desc] = {"message": f"failed - {i['message']}"}
    return results
