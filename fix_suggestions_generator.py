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

    # Formulate the prompt for OpenAI
    prompt = (
        f"Here is a bug in the code:\n\n"
        f"Code:\n{code_snippet}\n\n"
        f"Failed Test: {test}\n\n"
        f"Category: {category}\n"
        f"Item: {item}\n\n"
        f"Can you suggest a fix for the above code?\n\n"
        f"Please format your response as follows:\n"
        f"Suggested Fix:\n\n<Your suggestion here>\n"
        f"Example:\n"
        f"Suggested Fix:\n\nRefactor the function to handle edge cases properly. Update the error handling mechanism."
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

    print(completion.choices[0].message.content)

    return completion.choices[0].message.content
