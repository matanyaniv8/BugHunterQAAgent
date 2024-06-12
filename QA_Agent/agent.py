from tests.button_tests import run_tests_html_code as button_tests_html, run_url_tests as button_tests_url
from tests.link_tests import run_link_tests_html_code as link_tests_html, run_url_link_tests as link_tests_url


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
    else:
        print(f"Unknown test type: {test_type}")
        return

    # Combine results and write to files
    all_results = results
    all_filenames = [filename]

    for filename in all_filenames:
        with open(filename, "w") as file:
            for result in all_results:
                file.write(f"### {result['name']} ###\n")
                if test_type == "button":
                    file.write(f"Button Text: {result['button_text']}\n")
                else:
                    file.write(f"Link Text: {result['link_text']}\n")
                    file.write(f"Link Href: {result['link_href']}\n")
                file.write(f"Result: {result['outcome']}\n")
                file.write(f"Method: {result['test_method']}\n")
                file.write(f"Test Description: {result['test_description']}\n\n")


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
    web_path = '../Websites_Generator/generated_html/buggy_website.html'  # Replace this with the actual file path
    html_content = get_html_content(web_path)
    if html_content:
        run_tests_wrapper(html_content, test_type="button")
        run_tests_wrapper(html_content, test_type="link")

    url = 'https://themeforest.net/search/dummy'  # URL to test
    run_tests_wrapper(url, test_type="button")
    run_tests_wrapper(url, test_type="link")
