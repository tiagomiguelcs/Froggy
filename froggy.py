"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
"""
# To Use on-the-fly certificates please run Flask as follows: 
# flask run --cert=adhoc

from flask import Flask, render_template
from configparser import SafeConfigParser
__version__     = 0.1
framework       = Flask(__name__, template_folder='')

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


