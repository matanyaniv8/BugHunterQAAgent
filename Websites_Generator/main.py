from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import random

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


@app.post("/generate")
async def generate_html(selection: BugSelection):
    bug_html_snippets = {
        "missing_alt": [
            '<img src="image.jpg">',
            '<img src="photo.png">'
        ],
        "broken_link": [
            '<a href="nonexistent.html">Broken Link</a>',
            '<a href="404.html">Another Broken Link</a>'
        ],
        "missing_doctype": [
            '<html><head><title>Test</title></head><body></body></html>',
            '<html><body><p>Content without DOCTYPE</p></body></html>'
        ],
        "submit_button_no_action": [
            '<form><button type="button">Submit</button></form>',
            '<form><input type="button" value="Submit"></form>'
        ],
        "non_functional_tabs": [
            '''
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">Contact</a></li>
                <li><a href="#">About Us</a></li>
            </ul>
            '''
        ],
    }

    selected_snippets = [random.choice(bug_html_snippets[bug]) for bug in selection.bugs if bug in bug_html_snippets]
    generated_html = "\n".join(selected_snippets)

    # Save the generated HTML
    file_name = "buggy_website.html"
    file_path = os.path.join("generated_html", file_name)
    with open(file_path, "w") as file:
        file.write(generated_html)

    # Return the URL to the generated HTML file
    return {"url": f"http://127.0.0.1:8000/generated_html/{file_name}"}


# Serve the generated HTML files
from fastapi.staticfiles import StaticFiles
app.mount("/generated_html", StaticFiles(directory="generated_html"), name="generated_html")
