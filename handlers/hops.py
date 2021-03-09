"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's Route Management Handler
"""
from froggy import framework
from flask import Flask, request
from handlers.auth import authorized
from handlers.exceptions import BadRequest
from handlers.gadgets import print
import functools

def frogify(*route_args, **route_kwargs):
    """Custom froggy decorator that wraps the flask route decorator plus
    some other relevant froggy functions (e.g., authorization).
    Args:
        route_args: Non-keywords argumentos (e.g. 'A', 'B', ...)
        route_kwargs: Keyword Arguments (e.g. first='A', second='B', ...)
    """
    # Pop out all the keys that are part of the froggy configuration environment
    # leaving only those that are for the route decorator. 
    restricted = route_kwargs.pop('authorization', False)
    
    def outer(action_function):
        # Let's call the route decorator to map the request route
        @framework.route(*route_args, **route_kwargs)
        @functools.wraps(action_function)
        def inner(*f_args, **f_kwargs):
            # Check if the current frog has permissions to access this resource
            if restricted:
                if (not authorized(request)): 
                    # Authentication token MIA raise bad request
                    raise BadRequest(path=request.path,message="",error="Authorization Failure",status=401)
            #print("f_args="+str(f_args) + ", size="+str(len(f_args)))
            #print("f_kwargs="+str(f_kwargs) + "size=" + str(len(f_kwargs)))
            #print("action_function=" + str(action_function))
            return action_function(*f_args, **f_kwargs)
        return inner
    return outer
