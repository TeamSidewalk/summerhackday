from flask import Flask
from flask import request
from flask import Response
from flask import render_template
import json
import pprint
import requests
# from urllib.request import urlopen

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'Hello Leah!'

@app.route('/thing', methods=['GET'])
def get_thing():
    if request.method == 'GET':
        return 'I have a thing'

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/get_nonprofit_data', methods=['GET', 'POST'])
def get_nonprofit_data():
    ein = request.args.get('nonprofit_ein')
    url = 'https://projects.propublica.org/nonprofits/api/v1/organizations/' + ein + '.json'
    r = requests.get(url)
    return r.text

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
		if request.method == 'GET':
			return render_template('signup.html')
		else:
			name = request.args.get('p_name')
			return name

if __name__ == '__main__':
    app.run()
