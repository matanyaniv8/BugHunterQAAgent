import json
from openai import OpenAI

OPENAI_API_KEY = ''
client = OpenAI(api_key=OPENAI_API_KEY)


def ask_openai_jason(model, prompt):
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
        response_json = json.loads(response_text)
    except json.JSONDecodeError:
        print("Could not parse response as JSON. Returning as plain text.")
        response_json = {"response": response_text}

    return response_json


def get_buggy_code_snippet(bugs: [str]):
    prompt = f"""
    Please generate HTML code snippets that intentionally contain these bug {bugs}. Each snippet should represent a common web development issue as described below. Ensure each type of bug is clearly identifiable within its snippet.

1. **Forms Input Elements Bugs**: Create a form with input elements where some inputs lack proper labels, making them less accessible and potentially causing confusion in form usage.

2. **Forms Submission Bugs**: Generate a form snippet where the submission button does not trigger any action due to a missing form action or incorrect method attribute.

3. **Buttons Visibility and Interactivity Issues**: Produce an HTML snippet with multiple buttons. Some buttons should be hidden via CSS, others should be overlapped by other elements making them non-interactable, and one button, when clicked, should cause a JavaScript error.

4. **Link Issues**: Create a snippet with several anchor tags where:
   - One link has no 'href' attribute.
   - Another link leads to a non-existent resource (broken link).
   - One uses an incorrect anchor linking method, such as a missing ID on the target element.
   - Include a JavaScript link that triggers an error when clicked.

For each bug, ensure the snippet is self-contained and simple enough to clearly demonstrate the specific issue, 
and please add in-tag styling for better representation.

### Example Output for One of the Requests:
<!-- Forms Submission Bugs Example -->
<form>
    <input type="text" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <!-- Notice the submit button has a missing 'type' attribute, and the form lacks 'action' -->
    <button>Submit</button>
</form>
```
Additional Details:
Each snippet should be wrapped in appropriate HTML tags but should not include the <html>, <body>, or <head> tags as they are presumed to be part of an existing page.
Each bug should be evident to a developer inspecting the code but may not be immediately obvious to a user interacting with the page.
Please generate each requested snippet following the guidelines provided for the respective bugs, and returns in a Jason format [bugs_snippet:  your html_code bugs]
    """
