import urllib.request
try:
    response = urllib.request.urlopen("http://127.0.0.1:5050/static/gestures/1.png")
    print("Status:", response.status)
except Exception as e:
    print("Error:", e)
