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
# APP SETUP — paths must be set BEFORE anything uses them
# ============================================================
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS) / "api"
else:
    BASE_DIR = Path(__file__).resolve().parent

UI_DIR   = BASE_DIR / "Ui"
TOOL_DIR = BASE_DIR / "Tools"

templates = Jinja2Templates(directory=str(UI_DIR / "templates"))
sarabunLM = TOOL_DIR / "SarabunLM.py"

if sarabunLM.exists():
    print(f"SarabunLM found: {sarabunLM}")
else:
    print(f"SarabunLM NOT found at: {sarabunLM}")

# When frozen, sys.executable is the .exe itself — not python.
# Use the bundled script path directly instead of subprocess.
env = os.environ.copy()
env["AI_OUTPUT"]    = "This is a test output from SarabunLM.py."
env["TEMPLATE_KEY"] = "ResearchPaper"

if not getattr(sys, 'frozen', False):
    # Only run as subprocess in dev mode
    result = subprocess.run(
        [sys.executable, str(sarabunLM)],
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return code:", result.returncode)

print("Tools dir:", TOOL_DIR)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return FileResponse(UI_DIR / "app.js", media_type="application/javascript")

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
@app.get("/api/Tools/LLM/DataStorage/outputs/output.pdf")
def get_output_pdf():
    pdf_path = TOOL_DIR / "LLM" / "DataStorage" / "outputs" / "output.pdf"
    if pdf_path.exists():
        return FileResponse(pdf_path, media_type="application/pdf")
    raise HTTPException(status_code=404, detail="PDF not found.")

app.mount("/api/Ui", StaticFiles(directory=str(UI_DIR)), name="ui")