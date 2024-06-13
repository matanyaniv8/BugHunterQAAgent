import os
from pathlib import Path

from tests.button_tests import run_tests_html_code as button_tests_html, run_url_tests as button_tests_url
from tests.link_tests import run_link_tests_html_code as link_tests_html, run_url_link_tests as link_tests_url
from tests.form_tests import run_tests_html_code as form_test_html, run_form_tests
from urllib.parse import urlparse

import nest_asyncio

nest_asyncio.apply()


async def run_tests_wrapper(web_data, filename):
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

    # Run button tests
    if is_url:
        button_results, _ = await button_tests_url(web_data)
        form_results, _ = await run_form_tests(web_data)
        link_results, _ = await link_tests_url(web_data)
    else:
        button_results, _ = await button_tests_html(web_data)
        link_results, _ = await link_tests_html(web_data)
        form_results, filename = await form_test_html(web_data)

    await write_results_to_file(button_results, filename, "button")
    await write_results_to_file(link_results, filename, "link")
    await write_results_to_file(form_results, filename, "form")

    # file_content = Path(filename).read_text(encoding='utf-8')
    # print(file_content)
    return ["hello"]


async def write_results_to_file(results, filename, test_type):
    """
    Writes the test results to a file.
    :param results: Test results.
    :param filename: Name of the file to write to.
    :param test_type: Type of test - "button", "link", or "form".
    """
    with open(filename, 'a') as file:
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
                        file.write(f"    {test}: {outcome}\n\n")


async def get_html_content(file_path):
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


async def execute_html_tests(file_path):
    """
    Runs the tests on the given HTML file and returns the results filepath.
    :param file_path: Path to the HTML file.
    :return: Path to the results file.
    """
    html_content = await get_html_content(file_path)
    if html_content:
        results_file = f"results/{os.path.basename(file_path).replace('.html', '')}_tests.html"
        await run_tests_wrapper(html_content, results_file)
        return results_file
    return None


async def execute_url_tests(url):
    """
    Runs the tests on the given URL and returns the results filepath.
    :param url: URL to run the tests on.
    :return: Path to the results file.
    """
    results_file = f"results/{get_domain_from_url(url)}_tests.txt"
    res = await run_tests_wrapper(url, results_file)
    return res


if __name__ == "__main__":
    import asyncio

    # Example usage for an HTML file
    html_file_path = 'generated_html/buggy_website.html'
    result_file_path = asyncio.run(execute_html_tests(html_file_path))
    print(f"Results written to: {result_file_path}")

    # Example usage for a URL
    # url = "https://www.mako.co.il/collab/N12_Contact.html?partner=NewsfooterLinks&click_id=esDU5sDbdL"
    # result_file_path = asyncio.run(execute_url_tests(url))
    # print(f"Results written to: {result_file_path}")
