"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's Exceptions Handler
"""
from datetime import datetime
import flask, froggy

class BadRequest(froggy.framework.Framework, Exception):
    """BadRequest class, the name says it all.
    """
    def __init__(self, **kwargs):
        self.path       = kwargs.get('path', None)
        self.message    = kwargs.get('message', None)
        self.operation  = kwargs.get('operation', None)
        self.status     = kwargs.get('status', 500)
        self.error      = kwargs.get('error', None) # Short error name (e.g., Internal Server Error)
        self.API        = kwargs.get('API', None) # The error is originated from... (e.g. froggy's database API).
        self.debug      = bool(kwargs.get('debug', False))

# @froggy.app.errorhandler(froggy.exceptions.BadRequest)
def handle_bad_request(error):
    """ Catch BadRequest exception globally, serialize into JSON with the json_response() function.

     Args:
        error(BadRequest): Python dictionary that should include the following key:value pairs:
            [status]     - HTTP status codes (e.g., 403)
            [error]      - A short description of the error
            [message]    - A description of the error
            path         - Service endpoint (use, request.path)
    """
    data={"timestamp" : datetime.utcnow().strftime('%d/%m/%y %H:%M:%S,%f')[:-3]}
    # Create Python Dictionary to hold the data related to the error.
    if error.message is not None:
        data["message"] = error.message
    
    if error.path is not None:
        data["path"] = error.path
    
    if error.error is not None:
        data["error"] = error.error

    if error.operation is not None:
        data["operation"] = error.operation

    # Internal debugger
    if (error.debug): print(str(data))
     
    # "Roads? Where We’re Going, We Don’t Need Roads."
    return error.response(data, status=error.status)
