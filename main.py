import nest_asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List
import os
import random
from fastapi.staticfiles import StaticFiles
from qa_agent import execute_url_tests, execute_html_tests
from system.bug_families.button_bugs import button_bugs
from system.bug_families.link_bugs import link_bugs
from system.bug_families.image_bugs import image_bugs
from system.bug_families.tab_bugs import tab_bugs
from system.bug_families.form_bugs import forms_bugs

# Apply nest_asyncio
nest_asyncio.apply()

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

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/generate")
async def generate_html(selection: BugSelection):
    # Combine all bug dictionaries
    bug_html_snippets = {
        **button_bugs,
        **link_bugs,
        **image_bugs,
        **tab_bugs,
        **forms_bugs,
    }

    selected_snippets = [random.choice(bug_html_snippets[bug]) for bug in selection.bugs if bug in bug_html_snippets]
    generated_html = "\n".join(selected_snippets)

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
async def test_html(file: FilePath):
    results_file = execute_html_tests(file.file_path)
    return {"results_path": results_file}


@app.post("/test_url")
async def test_url(url_data: UrlData):
    url = str(url_data.url)  # Convert URL to string
    try:
        results_file = await execute_url_tests(url)
        return {"results_path": results_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
