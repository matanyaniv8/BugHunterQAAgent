import os
from tests.button_tests import run_tests_html_code as button_tests_html, run_url_tests as button_tests_url
from tests.link_tests import run_link_tests_html_code as link_tests_html, run_url_link_tests as link_tests_url
from tests.form_tests import run_form_tests
from urllib.parse import urlparse


def run_tests_wrapper(web_data, filename):
    """
    Wrapper function for running tests on buttons, links, and forms.
    Writes the results into a single file.
    :param web_data: HTML code or URL.
    :param filename: Name of the file to write to.
    """
    # Remove file if it exists
    if os.path.exists(filename):
        os.remove(filename)

    is_url = web_data.startswith("http")
    form_results = []

    # Run button tests
    if is_url:
        # button_results, _ = button_tests_url(web_data)
        button_results = []
        link_results, _ = link_tests_url(web_data)
        form_results = run_form_tests(web_data)
        # write_results_to_file(button_results, filename, "form")
    else:
        button_results, _ = button_tests_html(web_data)
        link_results, _ = link_tests_url(web_data)

    write_results_to_file(button_results, filename, "button")
    write_results_to_file(link_results, filename, "link")
    write_results_to_file(form_results, filename, "form")


def write_results_to_file(results, filename, test_type):
    """
    Writes the test results to a file.
    :param results: Test results.
    :param filename: Name of the file to write to.
    :param test_type: Type of test - "button", "link", or "form".
    """
    with open(filename, "a") as file:
        file.write(f"########## {test_type.upper()} TESTS ##########\n\n")

        if not results:
            file.write("No results found.\n\n")
            return

        if test_type == "form":
            for test in results:
                title, result = test
                file.write(f"######## {title} ########\n\n")

                for res in result:
                    file.write(f"### {res.get('name', 'Unnamed Test')} ###\n")
                    file.write(f"Option Text: {res.get('button_text', 'N/A')}\n")
                    file.write(f"Outcome: {res['outcome']}\n")
                    file.write(f"Test Method: {res['test_method']}\n")
                    file.write(f"Test Description: {res['test_description']}\n\n")
        else:
            for result in results:
                file.write(f"### {result.get('name', 'Unnamed Test')} ###\n")
                if test_type == "button":
                    file.write(f"Button Text: {result.get('button_text', 'N/A')}\n")
                    file.write(f"Result: {result.get('outcome', 'N/A')}\n")
                elif test_type == "link":
                    file.write(f"Link Text: {result.get('link_text', 'N/A')}\n")
                    file.write(f"Link Href: {result.get('link_href', 'N/A')}\n")
                    for test, outcome in result.get('outcomes', {}).items():
                        file.write(f"    {test}: {outcome}\n")


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


if __name__ == "__main__":
    web_path = '../Websites_Generator/generated_html/buggy_website.html'
    html_content = get_html_content(web_path)
    if html_content:
        # run_tests_wrapper(html_content, filename={f"websitesTestResult/buggy_website_tests.html"})
        pass

    url = "https://www.mako.co.il/collab/N12_Contact.html?partner=NewsfooterLinks&click_id=esDU5sDbdL"
    run_tests_wrapper(url, f"websitesTestsResult/{get_domain_from_url(url)}_tests.text")
