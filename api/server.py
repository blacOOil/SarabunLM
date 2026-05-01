
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