import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello from pod {os.environ.get("POD_NAME")}!'

@app.route('/webhook', methods=['POST'])
def post_data():
    data = request.get_json()
    if 'pull_request' in data and 'action' in data:
        pr = data['pull_request']
        action = data['action']
        if action == 'opened':
            # todo handle pr opened
            print(f"PR {pr['number']} created by {pr['user']['login']}")
        elif action == 'edited':
            # todo handle pr edited
            print(f"PR {pr['number']} edited by {pr['user']['login']}")
    result = {'status': 'success'}
    return jsonify(result)

if __name__ == '__main__':
    app.run()
