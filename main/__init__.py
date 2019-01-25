from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

@app.route('/jd_root.txt')
def jd_verify():
    return 'e95d2f4a675fe6f2b231093ef0892219c03e13e310499f23'
