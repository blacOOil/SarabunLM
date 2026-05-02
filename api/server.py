import subprocess
import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import api.Tools.DocFormat as DocFormat

# ============================================================
# APP SETUP
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
UI_DIR   = BASE_DIR / "Ui"
TOOL_DIR = BASE_DIR / "Tools"

templates = Jinja2Templates(directory=str(UI_DIR / "templates"))

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(UI_DIR)), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Tools dir:", TOOL_DIR)

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
# ROUTES — STATIC FILES
# ============================================================
@app.get("/")
def index():
    return FileResponse(UI_DIR / "templates" / "index.html")

@app.get("/api/Ui/style.css")
def get_style():
    return FileResponse(UI_DIR / "style.css")

@app.get("/api/Ui/app.js")
def get_script():
    return FileResponse(UI_DIR / "app.js")

@app.get("/favicon.ico")
def favicon():
    favicon_path = UI_DIR / "favicon.ico"
    if favicon_path.exists():
        return FileResponse(favicon_path)
    return Response(status_code=204)

# ============================================================
# ROUTES — CONFIG
# ============================================================
@app.get("/config")
def get_config():
    try:
        config = DocFormat.Config_Document_Format
        if not config:
            raise HTTPException(status_code=404, detail="Config not found.")
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# ROUTES — GENERATE
# ============================================================
@app.post("/generate")
def generate(data: GenerateRequest):
    env = os.environ.copy()
    env["AI_OUTPUT"] = data.ai_output

    result = subprocess.run(
        [sys.executable, str(TOOL_DIR / "SarabunLM.py")],
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr.strip())

    return {"message": "Document generated successfully."}