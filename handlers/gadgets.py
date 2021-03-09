"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's Gadgets or Utility Belt.
"""
from froggy import framework, __version__
from flask import Flask, request, jsonify

def improved_print(func):
    """Use a decorator to add some "sparkle" to the print function, froggy needs some blush!
    Args:
        func: Function name
    """
    def wrapper(*args,**kwargs):
        return func("[Froggy]:",*args,**kwargs)
    return wrapper

print = improved_print(print)

def json_response(data=None, **kwargs):
    """Creates a JSON response object built around the data python dictionary.
    
    Args:
        data: The Python dictionary containing the data for the JSON response object
        kwargs:
    
    Returns:
        JSON response object.
    """
    try:
        debug = bool(kwargs.get('debug', False))
    except KeyError:
        debug = False
    if (debug): print(data)
    if (data is not None):
        data["froggy"] = __version__
    else:
        data = {
            "froggy": __version__,
            "status": 200
        }
    
    # Creates a Response with the JSON representation of data
    return jsonify(data)