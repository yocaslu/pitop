from flask import Flask, Response
from modules.system import RASPBERRY_PY
import json
app = Flask(__name__)

@app.route("/")
def home():
    return Response(
        json.dumps(RASPBERRY_PY.to_dict(), indent=2),
        mimetype = "application/json"
    )