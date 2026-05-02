import threading
import time
import sys
import os
import uvicorn
import webbrowser
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from api.server import app as sarabun_app

# ==========================
# CONFIG
# ==========================
HOST = "127.0.0.1"
PORT = 5000
RUN_MODE = "local"   # "local" or "browser"


def run_sarabun():
    uvicorn.run(
        sarabun_app,
        host=HOST,
        port=PORT,
        log_level="warning"
    )


def wait_for_server(host, port, timeout=10):
    """Poll until the server responds or timeout is reached."""
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
        print("pywebview is not installed.")
        print("Install it with: pip install pywebview")
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

    webview.start()


if __name__ == "__main__":

    # Optional CLI override
    if len(sys.argv) > 1:
        RUN_MODE = sys.argv[1].lower()

    print("Starting Sarabun API server...")

    server_thread = threading.Thread(
        target=run_sarabun,
        daemon=True
    )
    server_thread.start()

    if RUN_MODE == "browser":
        if not wait_for_server(HOST, PORT):
            print(f"Server did not respond at http://{HOST}:{PORT}. Aborting.")
            sys.exit(1)
        start_browser()

    elif RUN_MODE == "local":
        start_local_app()

    else:
        print("Invalid mode.")
        print("Use: python app.py [browser|local]")
        sys.exit(1)

    # Keep main thread alive for daemon server thread
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down.")
        sys.exit(0)