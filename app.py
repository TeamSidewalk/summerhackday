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

def do_signup():
	

def show_the_signin_form():


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
		if request.method == 'POST'
			do_signup()
		else
			show_the_signin_form()

if __name__ == '__main__':
    app.run()