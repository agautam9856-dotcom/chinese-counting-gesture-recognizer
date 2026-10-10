from flask import Flask
import os
app = Flask(__name__, static_folder='demo', static_url_path='/static')
print("Static folder:", app.static_folder)
print("Files in static folder:", os.listdir(app.static_folder))
