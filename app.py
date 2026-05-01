import threading
import subprocess
import time
import sys
import os
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from api.server import app as sarabun_app

def run_sarabun():
    uvicorn.run(sarabun_app, host="127.0.0.1", port=5000, log_level="warning")

if __name__ == "__main__":
    try:
        import webview
    except ImportError:
        print("pywebview is not installed. Please install it using 'pip install pywebview'")
        sys.exit(1)

    print("Starting Sarabun API server...")
    t = threading.Thread(target=run_sarabun, daemon=True)
    t.start()
    
    time.sleep(1.0)  # Increased slightly to ensure Uvicorn is ready

    print("Opening webview...")
    
    # Fixed: Added commas after each argument
    webview.create_window(
        title="SarabunLM", 
        url="http://127.0.0.1:5000",
        width=1024,
        height=768,
        resizable=False,
        on_top=False,
        background_color="#393939"
    )
    
    webview.start()
    print("Webview closed. Shutting down server...")