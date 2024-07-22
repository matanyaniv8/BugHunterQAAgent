import json
from openai import OpenAI

from system.bug_families.button_bugs import button_bugs
from system.bug_families.form_bugs import forms_bugs
from system.bug_families.link_bugs import link_bugs
from system.bug_families.tab_bugs import tab_bugs

with open('openAI_Key', 'r') as file:
    OPENAI_API_KEY = file.read().strip()
    print(f"Read Open AI API Key successfully! - {OPENAI_API_KEY}")

client = OpenAI(api_key=OPENAI_API_KEY)

bugs_descriptions = {
    'submit_button_no_action': f"submit_button_no_action - A submit button that does nothing when clicked. "
                               f"for example {button_bugs['submit_button_no_action']}",

    'empty_button': f"empty_button - A button that appears empty and does nothing and does not have text on it. "
                    f"for example {button_bugs['empty_button']}",
    'non_functional_tabs': f"non_functional_tabs - Tab elements that look clickable but have no functionality. for "
                           f"example {tab_bugs['non_functional_tabs']}",
    'broken_link': f"broken_link - A hyperlink that leads to a non-existent page. "
                   f"for example {link_bugs['broken_link']}",
    'non_visible_link': f"non_visible_link - A link that is present in the code but not visible on the page. "
                        f"for example {link_bugs['non_visible_link']}",
    'no_href_link': f"no_href_link - A hyperlink element without an href attribute. "
                    f"for example {link_bugs['no_href_link']}",
    'javascript_link': f"javascript_link - A link that executes JavaScript code incorrectly. "
                       f"for example {link_bugs['javascript_link']}",
    'incorrect_anchor_link': f"incorrect_anchor_link - A link that refers to a non-existent anchor on the same page. "
                             f"for example {link_bugs['incorrect_anchor_link']}",
    'inputs buttons': f"inputs buttons - Input elements styled as text area, some inputs have type=number "
                      f"for email, password, checkboxes but are non fully interactive. "
                      f"for example {forms_bugs['inputs buttons']}",
    'Drop-Down list selection validation': f"Drop-Down list selection validation"
                                           f" - A drop-down list that does not validate or react to user selection. "
                                           f"for example {forms_bugs['Drop-Down list selection validation']}",
    'combined': f"Input elements styled as text area for email, password, checkboxes but are non fully interactive,  "
                f"and a drop-down list that does not validate or react to user selection. "
                f"for example {forms_bugs['combined']}",
}


def ask_openai_json(model, prompt, buggy_code_req=True):
    """
    Send a request to OpenAI API with a specific model and prompt,
    returning the response in JSON format.

    :param model: The model to use (e.g., 'gpt-3.5-turbo').
    :param prompt: The prompt message to ask the API.
    :return: JSON-formatted response.
    """
    # Build the conversation messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # Send the chat completion request to OpenAI
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )

    # Extract the content of the response
    response_text = completion.choices[0].message.content

    # Try to parse the response into JSON
    try:
        # response_json = json.loads(response_text)
        response_json = response_text if not buggy_code_req else json.loads(response_text)
    except json.JSONDecodeError:
        print("Could not parse response as JSON. Returning as plain text.")
        if buggy_code_req:
            response_json = {"response": response_text.split("response")[-1][4:-7]}
        else:
            response_json = {response_text.strip().replace('\\*', "").split("response")[-1]}

    return response_json


def get_bugs_description(bugs: [str]):
    description = ""
    for idx, bug in enumerate(bugs, start=1):
        bug_description = bugs_descriptions.get(bug, '')
        if bug_description != '':
            description += f"{idx}. {bug_description}\n"
    return description


def get_buggy_code_snippet(bugs: [str], file_path='./generated_html/buggy_code1.html'):
    # Read the file content into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Define the returned format
    returned_format = "{response : html_code}"
    prompt = f"""Take this html code, and the following html snippets that represents a buggy code, and generate buggy code and embeded it into the given website.
    please return only the html content in a json format {returned_format}. PLEASE KEEP THE SAME GIVEN WEBSITE WITH IT'S STYLE AND IT'S ELEMENT, ONLY 
    EMBED THE NEW CODE INSIDE OF THE GIVEN WEBSITE.
    
    the website is : {file_content}
    The List of bugs are:\n{get_bugs_description(bugs)}
"""

    answer = ask_openai_json(model="gpt-3.5-turbo", prompt=prompt, buggy_code_req=True)['response']

    answer = answer.replace('\\n', "")  # for dealing with \n
    answer = answer.replace('\\', "")
    print(answer)
    return answer


# prompt = f""" Generate a nice looking webpage with nice elements that embedded the following html code snippets that visually demonstrate various common web development bugs. Each
# snippet should include a single bug from the provided list and apply CSS styling to ensure that the snippet is
# not visually boring. Each HTML snippet should clearly represent the bug in isolation so that it can be easily
# identified and understood.
# make sure that you give a buggy code for each bug!


# List of bugs to be included in the HTML snippets:\n{get_bugs_description(bugs)}
# Please ensure each snippet is contained within the same <div> with a class name corresponding to the bug type and apply
# minimal CSS styling to make each snippet visually interesting. For example, use colors, borders, or padding. \nAlso
# note that you should not include the <html>, <body>, or <head> tags as they are presumed to be part of an existing
# page. please return with the format {returned_format} where you put the combined code in one div in the html code
# field of the response format."""

if __name__ == '__main__':
    get_buggy_code_snippet(
        ['submit_button_no_action', 'empty_button', 'non_functional_tabs', 'broken_link', 'non_visible_link',
         'no_href_link', 'javascript_link', 'incorrect_anchor_link', 'inputs buttons',
         'Drop-Down list selection validation'], './generated_html/buggy_code1.html')
