from flask import Flask, send_from_directory
import threading
import urllib.request
import time

app = Flask(__name__)

@app.route('/assets/gestures/<path:filename>')
def serve_gesture(filename):
    return send_from_directory('demo/gestures', filename)

def run():
    app.run(port=5050)

t = threading.Thread(target=run)
t.daemon = True
t.start()
time.sleep(2)

try:
    response = urllib.request.urlopen("http://127.0.0.1:5050/assets/gestures/1.png")
    print("Status:", response.status)
except Exception as e:
    print("Error:", e)
