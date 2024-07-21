import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List
import os
import random
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

from qa_agent import execute_url_tests, execute_html_tests
from system.bug_families.button_bugs import button_bugs
from system.bug_families.link_bugs import link_bugs
from system.bug_families.tab_bugs import tab_bugs
from system.bug_families.form_bugs import forms_bugs
from buggy_code_generator import get_buggy_code_snippet, ask_openai_json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BugSelection(BaseModel):
    bugs: List[str]


class FilePath(BaseModel):
    file_path: str


class UrlData(BaseModel):
    url: HttpUrl


class TestData(BaseModel):
    category: str
    item: str
    test: str


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/generate")
def generate_html(selection: BugSelection):
    print("Generating buggy website...")
    bug_html_snippets = {
        **button_bugs,
        **link_bugs,
        **tab_bugs,
        **forms_bugs,
    }

    generated_html_snippets = get_buggy_code_snippet(selection.bugs)

    # Wrap in a complete HTML structure
    generated_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Buggy Website</title>
    </head>
    <body>
        {generated_html_snippets}
    </body>
    </html>
    """

    # Save the generated HTML
    file_name = "buggy_website.html"
    file_path = os.path.join("generated_html", file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(generated_html)
    # Return the URL to the generated HTML file
    return {"url": f"http://127.0.0.1:8000/generated_html/{file_name}"}


app.mount("/generated_html", StaticFiles(directory="generated_html"), name="generated_html")


@app.post("/test_html")
def test_html(file: FilePath):
    file_path = file.file_path
    results = execute_html_tests(file_path)
    print(results)
    return results  # get_suggestion(results)


@app.post("/test_url")
def test_url(url_data: UrlData):
    url = str(url_data.url)
    results = execute_url_tests(url)
    return {"results": results}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join('uploaded_files', file.filename)
    print(file_location)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return JSONResponse(content={"message": "File uploaded successfully", "file_path": file_location})


# def get_suggestion(results):
#     return ""
#     prompt = """
#         only give me the results in a json format.
#        You are a helpful assistant. For every "failed" test in the given dictionary, add a possible solution in the same line and return the updated dictionary.
#         keep "passed" test Here is the input dictionary:
#        Input:
#        {results_dict}
#
#        Output should be the same dictionary with solutions added to failed tests. Solutions should be:
#        - For "Click Test: failed - Expected element not found after click": Ensure the expected element appears after the click by verifying the correct element locator and adding a wait condition if necessary.
#        - For "Visibility Test: failed - Button is hidden": Ensure the button is not hidden or covered by another element.
#        - For "Check Broken Link: FAILED - Status Code: 500": Investigate server issues or ensure the URL is correctly pointing to an existing resource.
#        - For "Check Responsive Link: FAILED - Status Code: 500": give me a possible solution.
#        """
#
#     # Prepare the prompt with the actual input dictionary
#     formatted_prompt = prompt.format(results_dict=results)
#
#     return ""


@app.post("/suggest_fix")
def suggest_fix(test_data: TestData):
    suggestion = execute_fix_suggestion(test_data.category, test_data.item, test_data.test)
    return {"suggestion": suggestion}


def execute_fix_suggestion(category: str, item: str, test: str) -> str:
    return "No specific fix suggestion available."
