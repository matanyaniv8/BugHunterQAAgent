import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

import fix_suggestions_generator
from qa_agent import execute_url_tests, execute_html_tests
from buggy_code_generator import get_buggy_code_snippet
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

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
    code_snippet: Optional[str]


@app.post("/generate")
def generate_html(selection: BugSelection):
    print("Generating buggy website...")
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
    return results


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


@app.post("/suggest_fix")
def suggest_fix(test_data: TestData):
    try:
        suggestion = fix_suggestions_generator.execute_fix_suggestion(
            test_data.category,
            test_data.item,
            test_data.test,
            test_data.code_snippet
        )
        return {"suggestion": suggestion}
    except Exception as e:
        print("Error during suggestion generation:", e)
        return {"suggestion": "Error during suggestion generation"}
