from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    file = open("../res/index.html")
    return file.read()

