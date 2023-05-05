import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello from pod {os.environ.get("POD_NAME")}!'
    
@app.route('/hello')
def hello_again():
    return f'Hello again from pod {os.environ.get("POD_NAME")}!'

if __name__ == '__main__':
    app.run()
