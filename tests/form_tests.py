from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def test_select_elements(page):
    """
    Loads the page and finds all the drop-down lists.
    Once found, checks each "select" element in the drop-down list to ensure it is visible
    and can be selected without any errors occurring afterward.
    :param page: The website loaded
    :return: Tests results.
    """
    results = []
    # Wait for the page to load completely
    page.wait_for_load_state('networkidle')

    selects = page.query_selector_all("select")

    for select_index, select in enumerate(selects):
        select_id = select.get_attribute('id') or select.get_attribute('name') or f'select{select_index + 1}'
        options = select.query_selector_all('option')
        options_text = [option.inner_text() for option in options]
        options_value = [option.get_attribute('value') for option in options]
        # Try selecting each option and capture any errors
        for i, option in enumerate(options):
            individual_test_name = f"Test for {select_id} Option {i + 1}"
            test_name = "Options select from list"
            try:
                if i == 0:
                    continue
                else:
                    is_option_disabled = option.is_disabled()
                    if not is_option_disabled:
                        select.select_option(index=i)
                        selected_option = select.query_selector("option:checked")

                        if selected_option.inner_text() == options_text[i] and not option.is_disabled():
                            outcome = "PASSED - No error on selection."
                        else:
                            outcome = (f"FAILED - Incorrect option selected. "
                                       f"Expected '{options_text[i]}', got {selected_option}")
                    else:
                        outcome = f"Failed - Option {options_text[i]} is disabled."

            except Exception as e:
                outcome = f"FAILED - Error on selection: {str(e)}"

            results.append({
                "name": individual_test_name,
                "button_text": options_text[i],
                "outcome": outcome,
                "test_method": test_name,
                "test_description": "Checks the functionality of a drop down list."
            })
    print(results)
    return results


def test_input_fields(form):
    """
    Evaluates and interacts with all input and textarea elements within a form:
    It fills text fields, checks checkboxes, and selects radio buttons as needed.
    :param form: Form to be evaluated.
    :return: Tests results for all inputs and fields.
    """
    results = []
    inputs = form.query_selector_all("input, textarea")
    for input in inputs:
        tag_name = input.evaluate("e => e.tagName.toLowerCase()")
        input_type = input.get_attribute("type") if tag_name == "input" else "textarea"

        if input_type in ["text", "password", "email", "textarea"]:
            input.fill("test")
        elif input_type == "checkbox":
            input.check()
        elif input_type == "radio":
            if not input.is_checked():
                input.check()

        result = {
            "name": tag_name if tag_name != "input" else input_type,
            "value": input.get_attribute("value"),
            "text": input.text_content(),
            "outcome": "PASSED - Filled or Checked",
            "test_method": "test_input_fields",
            "test_description": "Tests if text inputs, checkboxes, and radio buttons can be interacted with."
        }
        results.append(result)
    return results


def test_form_submission(form, page):
    """
    Checks Form "submit" button- if it has a values and when on-clicking, it doesn't trigger an error.
    :param form: Form to be evaluated.
    :param page: Page, which the form is submitted.
    :return: Tests results for the "submit" button.
    """
    submit_button = form.query_selector("input[type='submit'], button[type='submit']")
    outcome = {}

    if submit_button:
        submit_button.click()
        page.wait_for_load_state("networkidle")
        outcome = {
            "name": "Form Submission Test",
            "button_text": f"{submit_button.get_attribute('value')}",
            "outcome": "PASSED - Submitted",
            "test_method": "test_form_submission",
            "test_description": "Checks if the form can be submitted successfully."
        }
    else:
        outcome = {
            "name": "Form Submission Test",
            "button_text": "N/A",
            "outcome": "FAILED - No Submit Button",
            "test_method": "test_form_submission",
            "test_description": "Fails if no submit button is present."
        }
    return outcome


def test_all_forms(page):
    """
    A wrapper method for testing forms and all inputs fields.
    :param page: Page to be evaluated.
    :return: Tests results for all forms and input fields.
    """
    results = []
    forms = page.query_selector_all("form")
    for form_index, form in enumerate(forms):
        # Test all input fields for interactions
        input_results = test_input_fields(form)
        results.extend(input_results)
        # Test form submission
        submission_result = test_form_submission(form, page)
        submission_result["form_index"] = f"{form_index}"
        results.append(submission_result)

    return results


def update_results_file(title: str, results: list, filename: str, file_mode: str = 'w'):
    """
    Updates the results file with the results.
    :param title: Test type as the title.
    :param results: Tests results.
    :param filename: the file to write/append to.
    :param file_mode: 'a' or 'w' for appending or writing to file.
    :return: Nothing.
    """
    with open(filename, file_mode) as file:
        file.write(f"########## {title} ##########\n\n")
        for result in results:
            file.write(f"### {result.get('name', 'Unnamed Test')} ###\n")
            file.write(f"Option Text: {result.get('button_text', 'N/A')}\n")
            file.write(f"Outcome: {result['outcome']}\n")
            file.write(f"Test Method: {result['test_method']}\n")
            file.write(f"Test Description: {result['test_description']}\n\n")


def run_tests_html_code(html_content):
    """
    Runs all the tests for an HTML code.

    :param html_content: HTML content of the page.
    :return: Results of the button tests and the filename.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        title = page.title() or "test_page"
        filename = f"./results/{title}_button_tests.txt"
        results = [("Drop Down List Tests", test_select_elements(page)), ("Test all inputs", test_all_forms(page))]
        browser.close()
        return results, filename


def run_form_tests(page_url):
    """
    Gather all forms tests and run them.

    Parameters:
        page_url (str): The URL of the webpage to test.
    :return:
        The function does not return a value but writes results to a file.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(page_url)
        # Wait for the page to load completely
        page.wait_for_load_state('networkidle')

        # Check if there are any forms on the page
        # if page.query_selector("form"):
        parsed_url = urlparse(page_url)
        domain_name = parsed_url.hostname.replace("www.", "")
        domain_name = domain_name.replace('.', '-')
        filename = f"./results/{domain_name}_form_tests.txt"
        results = [("Drop Down List Tests", test_select_elements(page)), ("Test all inputs", test_all_forms(page))]

        # update_results_file("Drop Down List Tests", test_select_elements(page), filename, 'w')
        # update_results_file("Test all inputs", test_all_forms(page), filename, 'a')
        browser.close()

        return results, filename


if __name__ == "__main__":
    url = 'http://127.0.0.1:8000/generated_html/buggy_website.html'
    run_form_tests(url)
    # run_form_tests("https://help.market.envato.com/hc/en-us/requests/new")