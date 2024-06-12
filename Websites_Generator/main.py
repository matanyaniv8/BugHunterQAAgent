from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import random
from bug_families.button_bugs import button_bugs
from bug_families.link_bugs import link_bugs
from bug_families.image_bugs import image_bugs
from bug_families.tab_bugs import tab_bugs

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
    }

    selected_snippets = [random.choice(bug_html_snippets[bug]) for bug in selection.bugs if bug in bug_html_snippets]
    generated_html = "\n".join(selected_snippets)

    # Save the generated HTML
    file_name = "buggy_website.html"
    file_path = os.path.join("generated_html", file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
    with open(file_path, "w") as file:
        file.write(generated_html)

    # Return the URL to the generated HTML file
    return {"url": f"http://127.0.0.1:8000/generated_html/{file_name}"}


# Serve the generated HTML files
from fastapi.staticfiles import StaticFiles

app.mount("/generated_html", StaticFiles(directory="generated_html"), name="generated_html")
