import threading
import webview
from backend.app import create_app

def run_flask():
    app = create_app()
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )

if __name__ == "__main__":
    # Start Flask in background
    threading.Thread(target=run_flask, daemon=True).start()

    # Create native window
    webview.create_window(
        title="Campus Hub",
        url="http://127.0.0.1:5000",
        width=488,
        height=819,
        resizable=False
    )

    webview.start()
