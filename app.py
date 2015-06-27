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

@app.route('/nonprofit_signup')
def signup():
#    name = request.args.get('name')
#    name = request.form['name']
    name = "Khan Academy" 
    return render_template('nonprofit_signup.html',
                           name=name)

@app.route('/get_nonprofit_data', methods=['GET', 'POST'])
def get_nonprofit_data():
    # default status
    r = None
    _dict = {}
    name = request.form['nonprofit_name']
    ein = request.form['nonprofit_ein']
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
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()
