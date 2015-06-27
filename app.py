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

    if is_json(r):
        _dict = json.loads(r)
        if 'total_results' in _dict and (name or ein):
            if _dict['total_results'] == 0:
                r = "No results for your query. :C"
    else:
        r = "No nonprofit with EIN exists"

    return r

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

@app.route('/org_confirm')
def load_profile():
    # index categories with API index - 1 (since list will start at 0)
    categories = ["Arts, Culture & Humanities",
                  "Education",
                  "Environment and Animals",
                  "Health",
                  "Human Services",
                  "International, Foreign Affairs",
                  "Public, Societal Benefit",
                  "Religion Related",
                  "Mutual/Membership Benefit",
                  "Miscellaneous"]

    return render_template('nonprofit_confirm.html')

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()
