
import subprocess
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sys
import api.Tools.DocFormat as DocFormat
from pathlib import Path


# ============================================================
# APP SETUP
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "Ui" 
Tool_DIR = BASE_DIR / "Tools"
templates = Jinja2Templates(directory=str(UI_DIR / "templates"))

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(UI_DIR)), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Tools dir:", Tool_DIR )

# ============================================================
# MODELS
# ============================================================
class GenerateRequest(BaseModel):
    ai_output: str
class ConfigResponse(BaseModel):
    doc_format: str
    section_number: int
    section_names: dict
# ============================================================
# ROUTES
# ============================================================

@app.get("/")
def index():
    return FileResponse(os.path.join(BASE_DIR, "Ui/templates/index.html"))
@app.get("/api/Ui/style.css")
def get_style():
    return FileResponse(os.path.join(UI_DIR, "style.css"))
@app.get("/api/Ui/app.js")
def get_script():
    return FileResponse(os.path.join(UI_DIR, "app.js"))
@app.get("/config")
def get_config(data:ConfigResponse):
    config = DocFormat.Config_Document_Format.get(DocFormat.Doc_format)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found.")
    return {
        "doc_format": DocFormat.Doc_format,
        "section_number": DocFormat.Section_Number,
        "section_names": DocFormat.Section_Name
    }
@app.post("/config")
def update_config(config: ConfigResponse):
    DocFormat.Doc_format = config.doc_format
    DocFormat.Section_Number = config.section_number
    DocFormat.Section_Name = config.section_names
    return {"message": "Config updated successfully."}
@app.post("/generate")
def generate(data: GenerateRequest):
    env = os.environ.copy()
    env["AI_OUTPUT"] = data.ai_output

    result = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "Tools", "SarabunLM.py")],
        capture_output=True, text=True, timeout=30, env=env
    )

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr.strip())
    return {"message": "Document generated successfully."} 