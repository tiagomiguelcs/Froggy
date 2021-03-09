"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's Exceptions Handler
"""
import flask
from datetime import datetime
from froggy import framework
from handlers.gadgets import print, json_response

class BadRequest(Exception):
    """BadRequest class, the name says it all.
    """
    def __init__(self, *args, **kwargs):
        self.path       = kwargs.get('path', None)
        self.message    = kwargs.get('message', None)
        self.status     = kwargs.get('status', None)
        self.error      = kwargs.get('error', None) # Short error name (e.g., Internal Server Error)
        self.debug      = bool(kwargs.get('debug', False))

@framework.errorhandler(BadRequest)
def handle_bad_request(error):
    """Catch BadRequest exception globally, serialize into JSON with the json_response() function.

    Args:
        error: Python dictionary that should include the following key:value pairs:
               [status]     - HTTP status codes (e.g., 403)
               [error]      - A short description of the error
               [message]    - A description of the error
               path         - Service endpoint (use, request.path)
    """
    # Create Python Dictionary to hold the data related to the error.
    data = {
        "timestamp" : datetime.utcnow().strftime('%d/%m/%y %H:%M:%S,%f')[:-3],
        "status"    : error.status,
        "error"     : error.error,
        "message"   : error.message,
        "path"      : error.path,
        "debug"     : False
    }
    # Internal debugger
    if (error.debug): print(str(data))
    
    # "Roads? Where We’re Going, We Don’t Need Roads."
    return json_response(data)
