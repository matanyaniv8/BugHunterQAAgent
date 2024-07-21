import openai
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

# Load the OpenAI API key
with open('openAI_Key', 'r') as file:
    OPENAI_API_KEY = file.read().strip()
    openai.api_key = OPENAI_API_KEY
    print(f"Read Open AI API Key successfully! - {OPENAI_API_KEY}")


class TestData(BaseModel):
    category: str
    item: str
    test: str
    code_snippet: Optional[str]


def execute_fix_suggestion(category: str, item: str, test: str, code_snippet: Optional[str]) -> str:
    print("Generating fix...")
    print(f"Code snippet: {code_snippet}")

    prompt = (
        f"Here is a bug in the code:\n\n"
        f"Code:\n{code_snippet}\n\n"
        f"Failed Test: {test}\n\n"
        f"Category: {category}\n"
        f"Item: {item}\n\n"
        f"Can you suggest a fix for the above code?\n\n"
        f"Please provide your suggestion in plain text format. Avoid including HTML code or other special formatting characters. If the issue involves a URL, simply provide the corrected URL without additional formatting.\n\n"
        f"**Example Fix:**\n\n"
        f"If the link 'https://dummies-profileapi.dummies.com/v2/sso/login' is broken, replace it with a valid link. Contact your backend team to get the correct link URL. Once you have the link, update the href value with the correct URL.\n\n"
        f"Example:\n\n"
        f"Replace 'https://dummies-profileapi.dummies.com/v2/sso/login' with 'https://valid-link.com/v2/sso/login'."
    )

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant skilled in debugging HTML code snippets."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = openai.chat.completions.create(
            model="gpt-4",
            messages=messages)

    return completion.choices[0].message.content
