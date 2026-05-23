import webview
from threading import Thread
from app import app

def run_flask():
    app.run(debug=False)

Thread(target=run_flask).start()

webview.create_window(
    "Cyberbullying Detection System",
    "http://127.0.0.1:5000",
    width=1000,
    height=700
)

webview.start()