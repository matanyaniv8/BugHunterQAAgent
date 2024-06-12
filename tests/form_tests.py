from urllib.parse import urlparse
from playwright.async_api import async_playwright


async def test_select_elements(page):
    """
    Loads the page and finds all the drop-down lists.
    Once found, checks each "select" element in the drop-down list to ensure it is visible
    and can be selected without any errors occurring afterward.
    :param page: The website loaded
    :return: Tests results.
    """
    results = []
    # Wait for the page to load completely
    await page.wait_for_load_state('networkidle')

    selects = await page.query_selector_all("select")

    for select_index, select in enumerate(selects):
        select_id = await select.get_attribute('id') or await select.get_attribute('name') or f'select{select_index + 1}'
        options = await select.query_selector_all('option')
        options_text = [await option.inner_text() for option in options]
        options_value = [await option.get_attribute('value') for option in options]
        # Try selecting each option and capture any errors
        for i, option in enumerate(options):
            individual_test_name = f"Test for {select_id} Option {i + 1}"
            test_name = "Options select from list"
            try:
                if i == 0:
                    continue
                else:
                    is_option_disabled = await option.is_disabled()
                    if not is_option_disabled:
                        await select.select_option(index=i)
                        selected_option = await select.query_selector("option:checked")

                        if await selected_option.inner_text() == options_text[i] and not await option.is_disabled():
                            outcome = "PASSED - No error on selection."
                        else:
                            outcome = (f"FAILED - Incorrect option selected. "
                                       f"Expected '{options_text[i]}', got {await selected_option.inner_text()}")
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
    return results


async def test_input_fields(form):
    """
    Evaluates and interacts with all input and textarea elements within a form:
    It fills text fields, checks checkboxes, and selects radio buttons as needed.
    :param form: Form to be evaluated.
    :return: Tests results for all inputs and fields.
    """
    results = []
    inputs = await form.query_selector_all("input, textarea")
    for input in inputs:
        tag_name = await input.evaluate("e => e.tagName.toLowerCase()")
        input_type = await input.get_attribute("type") if tag_name == "input" else "textarea"

        if input_type in ["text", "password", "email", "textarea"]:
            await input.fill("test")
        elif input_type == "checkbox":
            await input.check()
        elif input_type == "radio":
            if not await input.is_checked():
                await input.check()

        result = {
            "name": tag_name if tag_name != "input" else input_type,
            "value": await input.get_attribute("value"),
            "text": await input.text_content(),
            "outcome": "PASSED - Filled or Checked",
            "test_method": "test_input_fields",
            "test_description": "Tests if text inputs, checkboxes, and radio buttons can be interacted with."
        }
        results.append(result)
    return results


async def test_form_submission(form, page):
    """
    Checks Form "submit" button- if it has a values and when on-clicking, it doesn't trigger an error.
    :param form: Form to be evaluated.
    :param page: Page, which the form is submitted.
    :return: Tests results for the "submit" button.
    """
    submit_button = await form.query_selector("input[type='submit'], button[type='submit']")
    outcome = {}

    if submit_button:
        await submit_button.click()
        await page.wait_for_load_state("networkidle")
        outcome = {
            "name": "Form Submission Test",
            "button_text": f"{await submit_button.get_attribute('value')}",
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


async def test_all_forms(page):
    """
    A wrapper method for testing forms and all inputs fields.
    :param page: Page to be evaluated.
    :return: Tests results for all forms and input fields.
    """
    results = []
    forms = await page.query_selector_all("form")
    for form_index, form in enumerate(forms):
        # Test all input fields for interactions
        input_results = await test_input_fields(form)
        results.extend(input_results)
        # Test form submission
        submission_result = await test_form_submission(form, page)
        submission_result["form_index"] = f"{form_index}"
        results.append(submission_result)

    return results


async def update_results_file(title: str, results: list, filename: str, file_mode: str = 'w'):
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


async def run_tests_html_code(html_content):
    """
    Runs all the tests for an HTML code.

    :param html_content: HTML content of the page.
    :return: Results of the button tests and the filename.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html_content)
        title = await page.title() or "test_page"
        filename = f"./results/{title}_button_tests.txt"
        results = [("Drop Down List Tests", await test_select_elements(page)), ("Test all inputs", await test_all_forms(page))]
        await browser.close()
        return results, filename


async def run_form_tests(page_url):
    """
    Gather all forms tests and run them.

    Parameters:
        page_url (str): The URL of the webpage to test.
    :return:
        The function does not return a value but writes results to a file.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(page_url)
        # Wait for the page to load completely
        await page.wait_for_load_state('networkidle')

        # Check if there are any forms on the page
        # if page.query_selector("form"):
        parsed_url = urlparse(page_url)
        domain_name = parsed_url.hostname.replace("www.", "")
        domain_name = domain_name.replace('.', '-')
        filename = f"./results/{domain_name}_form_tests.txt"
        results = [("Drop Down List Tests", await test_select_elements(page)), ("Test all inputs", await test_all_forms(page))]

        # update_results_file("Drop Down List Tests", test_select_elements(page), filename, 'w')
        # update_results_file("Test all inputs", test_all_forms(page), filename, 'a')
        await browser.close()

        return results, filename

