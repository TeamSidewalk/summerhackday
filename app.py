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
    ein = request.form['nonprofit_ein']
    url = 'https://projects.propublica.org/nonprofits/api/v1/organizations/' + ein + '.json'
    r = requests.get(url)
    return r.text

@app.route('/signup')
def sign_up():
        return render_template('signup.html');

if __name__ == '__main__':
    app.run()
