"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
"""
# To Use on-the-fly certificates please run Flask as follows: 
# flask run --cert=adhoc
# In order to use apidoc you need to install it npm install -g apidoc
from flask import Flask, render_template, redirect, url_for
from configparser import SafeConfigParser
import os
__version__     = 0.1
framework       = Flask(__name__, template_folder='', static_url_path='')

parser = SafeConfigParser()
parser.read('config.cfg')
JWT_SECRET_TOKEN                            = parser.get('DEFAULT', 'JWT_SECRET_TOKEN')
JWT_EXPIRATION_SECONDS                      = parser.get('DEFAULT', 'JWT_EXPIRATION_SECONDS')

import examples.auth
import examples.hello_world
import handlers.hops

@framework.route('/')
def home():
    return render_template('froggy.html', version=__version__)

@framework.route('/docs')
def documentation():
    return redirect(url_for("static", filename="docs/index.html"))

if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    print("""\
                  _e-e_
                _(-._.-)_
             .-(  `---'  )-. 
            __\ \\\___/// /__
           '-._.'/M\ /M\`._,-
    Froggy - The Python Rest Framework""")
# Update the froggy documentation using the awesome open source projet apiDoc (https://github.com/apidoc/apidoc). 
os.system('apidoc -i ./examples/ -o ./static/docs')
