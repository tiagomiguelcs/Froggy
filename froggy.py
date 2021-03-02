from flask import Flask, render_template
VERSION = 0.1;
froggy  = Flask(__name__, template_folder='');


@froggy.route('/')
def home():
    return render_template('froggy.html', version=VERSION);
