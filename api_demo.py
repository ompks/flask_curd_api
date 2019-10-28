
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/get_method', methods=['GET'])
def get_method():
    return ("Hello")

@app.route('/post_method', methods=['POST'])
def post_method():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
    return "Binary message written!"

app.run(host='localhost', port=8085, use_reloader=False)
