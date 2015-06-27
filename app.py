from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for
import json
import pprint
import requests
# from urllib.request import urlopen

app = Flask(__name__)
app.debug = True
app.secret_key = 'test'

@app.route('/thing', methods=['GET'])
def get_thing():
    if request.method == 'GET':
        return 'I have a thing'

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/nonprofit_signup')
def signup():
#    name = request.args.get('name')
#    name = request.form['name']
    name = session['name']
    return render_template('nonprofit_signup.html',
                           name=name)

@app.route('/get_nonprofit_data', methods=['POST'])
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
        session['_dict_exists'] = True
        if 'total_results' in _dict and (name or ein):
            if _dict['total_results'] == 0:
                session['_dict_exists'] = False
                session['_dict_errors'] = "No results for your query. :C"
    else:
        session['_dict_errors'] = "No nonprofit with EIN exists"
        session['_dict_exists'] = False

    session['_dict'] = _dict

    print _dict

    return redirect(url_for("load_profile"))

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

    if session['_dict_exists']:
        return render_template('nonprofit_confirm.html', _dict=session['_dict'])
    else:
        return session['_dict_errors']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/description')
def about():
    return render_template('description.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        print "does it get here?"
        return render_template('signup.html')
    else:
        print "how about here?"
        name = request.form['p_name']
        type = request.form['type']
        session['name'] = name
        if type == 'Non Profit':
            return redirect('/nonprofit_signup')#, name=name)
        else:
            return redirect('/')

if __name__ == '__main__':
    app.run()
