import requests
from bs4 import BeautifulSoup


def extract_buttons_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract <button> tags
    buttons = soup.find_all('button')

    # Extract <input> tags that function as buttons
    inputs = soup.find_all('input', {'type': ['button', 'submit', 'reset']})

    # Extract <a> tags that are styled as buttons
    anchors = soup.find_all('a', {'role': 'button'})

    # Combine all found elements
    all_buttons = list(buttons) + list(inputs) + list(anchors)
    return all_buttons


def extract_buttons_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return extract_buttons_from_html(response.content)
    else:
        return []


def check_button_visibility(button):
    test_name = "check_button_visibility"
    try:
        # Check if the button is not hidden (basic check)
        if 'hidden' not in button.attrs.get('style', ''):
            return test_name, "passed"
        else:
            return test_name, "failed - Button is hidden"
    except Exception as e:
        return test_name, f"failed - Exception: {e}"


def check_button_title(button):
    test_name = "check_button_title"
    try:
        # Check if the button has text or title
        if button.text.strip() or button.attrs.get('title'):
            return test_name, "passed"
        else:
            return test_name, "failed - Button has no title or text"
    except Exception as e:
        return test_name, f"failed - Exception: {e}"


def check_button_interactivity(button):
    test_name = "check_button_interactivity"
    try:
        # Basic check: button should have a type attribute or be clickable
        if button.name == 'button' or button.attrs.get('type') in ['button', 'submit', 'reset']:
            return test_name, "passed"
        elif button.name == 'a' and button.attrs.get('role') == 'button':
            return test_name, "passed"
        else:
            return test_name, "failed - Button is not interactive"
    except Exception as e:
        return test_name, f"failed - Exception: {e}"


def check_button_link(button):
    test_name = "check_button_link"
    try:
        # Check if the button leads to a link (basic check: does it have an onclick, href or form action)
        if 'onclick' in button.attrs or 'formaction' in button.attrs or button.attrs.get('href'):
            return test_name, "passed"
        else:
            return test_name, "failed - Button does not lead to any link"
    except Exception as e:
        return test_name, f"failed - Exception: {e}"


def run_tests_on_buttons(buttons):
    results = {}
    for button in buttons:
        button_text = button.text.strip() or button.attrs.get('title', 'no-title')
        results[button_text] = {}
        for check in [check_button_visibility, check_button_title, check_button_interactivity, check_button_link]:
            test_name, result = check(button)
            results[button_text][test_name] = result
    return results


def execute_button_tests(url):
    print(f"Start running button tests on {url}")
    all_buttons = extract_buttons_from_page(url)
    print(f"Extracted all buttons - total of {len(all_buttons)} buttons")
    results = run_tests_on_buttons(all_buttons)
    return results


def execute_button_html_tests(html_content):
    print(f"Start running button tests on provided HTML")
    buttons = extract_buttons_from_html(html_content)
    results = run_tests_on_buttons(buttons)
    return results
