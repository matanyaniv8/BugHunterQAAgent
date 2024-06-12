from tests.button_tests import run_tests_html_code as button_tests_html, run_url_tests as button_tests_url
from tests.link_tests import run_link_tests_html_code as link_tests_html, run_url_link_tests as link_tests_url
from tests.from_tests import run_form_tests


def run_tests_wrapper(web_data, test_type="button"):
    """
    Wrapper function for run_tests, if the website is an HTML code or an URL.
    Writes the results into a file.
    :param web_data: HTML code or URL.
    :param test_type: Type of test to run - "button" or "link".
    """
    if test_type == "button":
        if web_data.startswith("http"):
            results, filename = button_tests_url(web_data)
        else:
            results, filename = button_tests_html(web_data)
    elif test_type == "link":
        if web_data.startswith("http"):
            results, filename = link_tests_url(web_data)
        else:
            results, filename = link_tests_html(web_data)
    elif test_type == "form":
        # results, filename = (
            run_form_tests(web_data)
    else:
        print(f"Unknown test type: {test_type}")
        return

    # write_results_to_file(results, filename, test_type)


def write_results_to_file(results, filename, test_type):
    """
    Writes the test results to a file.
    :param results: Test results.
    :param filename: Name of the file to write to.
    :param test_type: Type of test - "button" or "link".
    """
    with open(filename, "w") as file:
        for result in results:
            file.write(f"### {result['name']} ###\n")
            if test_type == "button":
                file.write(f"Button Text: {result.get('button_text', 'N/A')}\n")
                file.write(f"Result: {result.get('outcome', 'N/A')}\n")
            else:
                file.write(f"Link Text: {result.get('link_text', 'N/A')}\n")
                file.write(f"Link Href: {result.get('link_href', 'N/A')}\n")
                for test, outcome in result.get('outcomes', {}).items():
                    file.write(f"    {test}: {outcome}\n")
            file.write(f"Overall Result: {result.get('overall_outcome', 'N/A')}\n\n")


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


if __name__ == "__main__":
    web_path = '../Websites_Generator/generated_html/buggy_website.html'
    html_content = get_html_content(web_path)
    if html_content:
        # run_tests_wrapper(html_content, test_type="button")
        run_tests_wrapper(html_content, test_type="link")

    # url = 'https://themeforest.net/search/dummy'
    url = "https://www.mako.co.il/collab/N12_Contact.html?partner=NewsfooterLinks&click_id=esDU5sDbdL"
    # run_tests_wrapper(url, test_type="button")
    # run_tests_wrapper(url, test_type="link")
    run_tests_wrapper(url, test_type="form")
