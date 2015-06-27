from flask import Flask
from flask import request
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'Hello Leah!'

@app.route('/thing', methods=['GET'])
def get_thing():
		if request.method == 'GET':
			return 'I have a thing'

if __name__ == '__main__':
    app.run()