from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

app = FastAPI()

# Mount static files (CSS, JS, images)
app.mount("/api/Ui", StaticFiles(directory="Ui"), name="Ui")

templates = Jinja2Templates(directory="Ui/templates")

@app.get("/")
async def home(request: Request):
   return templates.TemplateResponse(request=request, name="index.html", context={"title": "My Website"})

@app.get("/api/hello")
async def hello(name: str = "World"):
    return JSONResponse({"message": f"Hello, {name}!"})