from playwright.sync_api import sync_playwright


def test_all_forms(page):
    """
    Tests all forms on a given page for proper handling of input fields and form submissions.
    :param page: Playwright page object where forms are located.
    :return: A list of dictionaries with test results for each form.
    """
    results = []
    forms = page.query_selector_all("form")
    for form_index, form in enumerate(forms):
        # Retrieve all input, select, and textarea elements within the form
        inputs = form.query_selector_all("input, select, textarea")

        for input in inputs:
            input_type = input.get_attribute("type")
            tag_name = input.evaluate("e => e.tagName.toLowerCase()")

            if tag_name == "textarea":
                input.fill("This is a test.")
            elif tag_name == "select":
                options = input.query_selector_all("option")
                if options and len(options) > 1:
                    input.select_option({"index": 1})
            elif input_type in ["text", "password", "email"]:
                input.fill("testinput")
            elif input_type == "checkbox":
                input.check()
            elif input_type == "radio":
                input.check()

        # Attempt to submit the form
        submit_button = form.query_selector("input[type='submit'], button[type='submit']")
        if submit_button:
            submit_button.click()
            page.wait_for_load_state("networkidle")

        # Check for response validation by looking for error or success messages
        error_messages = form.query_selector_all(".error")
        success_message = form.query_selector(".success")

        if error_messages:
            error_texts = [error.text_content() for error in error_messages]
            result = {"form_index": form_index, "outcome": "FAIL", "errors": error_texts}
        elif success_message:
            result = {"form_index": form_index, "outcome": "PASS", "message": success_message.text_content()}
        else:
            result = {"form_index": form_index, "outcome": "UNKNOWN", "message": "No clear success/error message found"}

        results.append(result)
    return results


def run_form_tests(url):
    """
    Sets up a browser session, navigates to the given URL, and runs form tests.
    :param url: URL of the webpage to test.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)  # Set headless to False to see the browser action
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        form_results = test_all_forms(page)
        browser.close()
        return form_results


# Example usage
if __name__ == "__main__":
    url = 'http://127.0.0.1:8000/generated_html/buggy_website.html'
    results = run_form_tests(url)
    # for result in results:
    #     print(result)
