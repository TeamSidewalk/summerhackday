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
    # default status
    r = None
    _dict = {}
    name = request.args.get('nonprofit_name')
    ein = request.args.get('nonprofit_ein')
    url_name = 'https://projects.propublica.org/nonprofits/api/v1/search.json'
    url_ein = 'https://projects.propublica.org/nonprofits/api/v1/organizations/' + ein + '.json'

    # if given EIN, search with EIN first since unique
    if ein:
        r = requests.get(url_ein).text
    elif name:
        r = requests.get(url_name, {'q': name}).text
    if r:
        _dict = json.loads(r)
    else:
        r = json.dumps('No information to search with :C')

    if 'total_results' in _dict and (name or ein):
        if _dict['total_results'] <= 0:
            r = "No results for your query. :C"                                                
    return r

@app.route('/signup')
def sign_up():
		return render_template('signup.html');

if __name__ == '__main__':
    app.run()
