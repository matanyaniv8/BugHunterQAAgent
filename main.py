import shutil
import os
import asyncio
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import uvicorn
import random
import fix_suggestions_generator
from qa_agent import execute_url_tests, execute_html_tests
from buggy_code_generator import get_buggy_code_snippet

app = FastAPI()

# CORS middleware setup
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


@app.on_event("startup")
async def startup_event():
    print("Application startup")


@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutdown")


@app.post("/generate")
def generate_html(selection: BugSelection):
    print("Generating buggy website...")
    generated_html_snippets = get_buggy_code_snippet(selection.bugs)

    template_files = ["./generated_html/website_template1.html", "./generated_html/website_template2.html"]
    template_path = random.choice(template_files)
    with open(template_path, "r") as template_file:
        template_html = template_file.read()

    # Define the placeholder in the template where you want to insert the snippets
    placeholder = "<!-- INSERT BUGGY CODE HERE -->"

    # Insert the generated HTML snippets at the placeholder
    if placeholder in template_html:
        updated_html = template_html.replace(placeholder, generated_html_snippets)
    else:
        print("Placeholder not found in the template")
        return {"error": "Placeholder not found in the template"}

    # Save the updated HTML file
    file_name = "buggy_website.html"
    file_path = os.path.join("generated_html", file_name)
    with open(file_path, "w") as file:
        file.write(updated_html)

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
    try:
        file_location = os.path.join('uploaded_files', file.filename)
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return JSONResponse(content={"message": "File uploaded successfully", "file_path": file_location})
    except asyncio.CancelledError:
        print("Upload was cancelled")
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.post("/suggest_fix")
def suggest_fix(test_data: TestData):
    print(test_data)
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


if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("Manual interruption received (CTRL-C).")
    except asyncio.CancelledError:
        print("Async operations cancelled.")
    except Exception as e:
        print("Error during execution:", e)
    finally:
        print("Server is shutting down. Cleaning up resources...")
