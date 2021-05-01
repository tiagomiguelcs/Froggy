"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
"""
import os, pkg_resources
__version__ = pkg_resources.require("froggy")[0].version

# All the modules under the froggy package should be imported here
from . import framework
from . import gadgets
from . import exceptions
from . import authentication
from . import files
from . import database

if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    print("""\
                  _e-e_
                _(-._.-)_
             .-(  `---'  )-. 
            __\ \\\___/// /__
           '-._.'/M\ /M\`._,-
    App Powered by Froggy """ + __version__ + """ - The Python Rest Framework
    https://github.com/tiagomiguelcs/froggy
    """)