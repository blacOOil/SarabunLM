from pathlib import Path
import threading
import time
import sys
import os
import traceback

# ============================================================
# CRASH LOGGER — must be before any other imports that can fail
# ============================================================
if getattr(sys, 'frozen', False):
    log_path = os.path.join(os.path.dirname(sys.executable), "sarabun_error.log")
    _log_file = open(log_path, "w", buffering=1)  # line-buffered
    sys.stdout = _log_file
    sys.stderr = _log_file

# ============================================================
# MAIN IMPORTS — errors here will now be caught in the log
# ============================================================
try:
    import uvicorn
    import webbrowser
    import urllib.request
    import urllib.error
    from api.server import app as sarabun_app
except Exception:
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# PATH
# ============================================================
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

# ============================================================
# CONFIG
# ============================================================
HOST     = "127.0.0.1"
PORT     = 5000
RUN_MODE = "local"   # "local" or "browser"

# ============================================================
# SERVER
# ============================================================
def run_sarabun():
    uvicorn.run(
        sarabun_app,
        host=HOST,
        port=PORT,
        log_level="warning"
    )

def wait_for_server(host, port, timeout=10):
    url = f"http://{host}:{port}"
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except (urllib.error.URLError, OSError):
            time.sleep(0.2)
    return False

def start_browser():
    url = f"http://{HOST}:{PORT}"
    print(f"Opening browser: {url}")
    webbrowser.open(url)

def start_local_app():
    try:
        import webview
    except ImportError:
        print("pywebview is not installed. Run: pip install pywebview")
        sys.exit(1)

    if not wait_for_server(HOST, PORT):
        print(f"Server did not respond at http://{HOST}:{PORT}. Aborting.")
        sys.exit(1)

    print("Opening local desktop app...")
    webview.create_window(
        title="SarabunLM",
        url=f"http://{HOST}:{PORT}",
        width=1024,
        height=768,
        resizable=False,
        on_top=False,
        background_color="#393939"
    )
    webview.start(debug=True)

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            RUN_MODE = sys.argv[1].lower()

        print("Starting Sarabun API server...")

        server_thread = threading.Thread(target=run_sarabun, daemon=True)
        server_thread.start()

        if RUN_MODE == "browser":
            if not wait_for_server(HOST, PORT):
                print(f"Server did not respond at http://{HOST}:{PORT}. Aborting.")
                sys.exit(1)
            start_browser()

        elif RUN_MODE == "local":
            start_local_app()

        else:
            print("Invalid mode. Use: python app.py [browser|local]")
            sys.exit(1)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down.")
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)