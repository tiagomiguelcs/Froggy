"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
    Froggy's Home
"""
from flask import Flask, request, render_template, redirect, url_for, jsonify
from configparser import SafeConfigParser
import froggy, os, functools, subprocess, shlex

TEMPLATE_FOLDER = os.path.normpath(os.path.dirname(os.path.abspath(__file__))) + "/templates/"
        
class Framework:
    """Froggy's main class
    
    On initialization it will load Froggy settings along with the Flask application object
    """
    def __init__(self, app, settings):
        """[summary]

        Args:
            app (Flask): The Flask application object.
            settings (list): A python dictionary where froggy settings should be specified.
        """
        # Set froggy settings from the 'settings' dic.
        self.name               = settings['name']
        self.app_package        = settings['package'] # App name that is using froggy
        self.documentation      = settings['documentation']
        self.auth               = settings['authentication']['type']
        self.logo               = settings['logo']
        self.app_root           = froggy.gadgets.normpath(os.path.dirname(os.path.abspath(self.app_package)))
        if (app is not None): 
            self.app            = app

        """ 
        print("Logo             =" + str(self.logo))
        print("Name             =" + str(self.name))
        print("Package          =" + str(self.app_package))
        print("Documentation    =" + str(self.documentation))
        print("Authentication   =" + str(self.auth))
        print("Root             =" + str(self.app_root))
        """
        # Enable internal froggy's functions, such as auto generation of documentation using apidoc 
        # or provide authentication procedures like JSON Web Tokens (JWT).
        if (self.documentation): self.gen_docs()
        if (self.auth == froggy.authentication.JWTAuth):
            self.JWT_SECRET_TOKEN       = settings['authentication']['jwt_secret_token']
            self.JWT_EXPIRATION_SECONDS = settings['authentication']['jwt_expiration_seconds'] 
            self.auth = froggy.authentication.JWTAuth(self.JWT_SECRET_TOKEN, self.JWT_EXPIRATION_SECONDS)
        else:
            self.auth = None

        # 'Inject' errorHandlers and custom froggy routes into the Flask object 'self.app' 
        self.app.errorhandler(froggy.exceptions.BadRequest)(froggy.exceptions.handle_bad_request)
        self.app.route('/froggy')(self.home)

    def gen_docs(self):
        """[summary] Documentation Generator

        If enabled, documentation can be created for the services implemented using froggy using a nice and handy tool called apidoc. 
        Each service should be documented following the syntax documented in the usage section detailed in https://github.com/apidoc/apidoc.
        """
        docs_dir = os.path.join(self.app_root, "docs")
        try:
            os.mkdir(docs_dir)
        except: 
            pass
        os.system('apidoc -i '+ self.app_root +' -o ' + docs_dir)
 
    def frogify(self, *route_args, **route_kwargs):
        """Custom froggy decorator that wraps the flask route decorator plus.
        
        some other relevant froggy functions (e.g., authorization).

        Args:
            route_args: Non-keywords argumentos (e.g. 'A', 'B', ...)
            route_kwargs: Keyword Arguments (e.g. first='A', second='B', ...)
        """
        # Pop out all the keys that are part of the froggy configuration environment
        # leaving only those that are for the route decorator. 
        restricted = route_kwargs.pop('authorization', False)
        groups   = route_kwargs.pop('groups', None)
        # fprint("Selected groups ="+str(groups))
        def outer(action_function):
            # Let's call the route decorator to map the request route
            @self.app.route(*route_args, **route_kwargs)
            @functools.wraps(action_function)
            def inner(*f_args, **f_kwargs):
                # Check if the current frog has permissions to access this resource
                if restricted:
                    if (not self.auth.authorized(request)): 
                        # Authentication token MIA raise bad request
                        raise froggy.exceptions.BadRequest(path=request.path,message="User not authenticated, token invalid or expired.",error="Authorization Failure",status=403)
                    if (groups is not None):
                        if (not self.auth.in_group(request, groups)):
                            # User not part of the group allowed to access the target resource
                            raise froggy.exceptions.BadRequest(path=request.path,message="The group of the user has no access permissions",error="Authorization Failure",status=403)

                #print("f_args="+str(f_args) + ", size="+str(len(f_args)))
                #print("f_kwargs="+str(f_kwargs) + "size=" + str(len(f_kwargs)))
                #print("action_function=" + str(action_function))
                # 'Ogres are like onions.'
                return action_function(*f_args, **f_kwargs)
            # I don't have friends. I got family'
            return inner
            # 'Dude, where's my car?'
        return outer

    def response(self, data=None, **kwargs):
        """Creates a JSON response object built around the data python dictionary.
            
        Args:
            data (list): The Python dictionary containing the data for the JSON response object.
        
        Returns:
            JSON response object.
        """
        try:
            debug = bool(kwargs.get('debug', False))
        except KeyError:
            debug = False
        if (debug): print(data)
        if (data is not None):
            data["froggy"] = froggy.__version__
        else:
            data = {
               "froggy": froggy.__version__,
               "status": 200
            }
            
        # Creates a Response with the JSON representation of data
        # 'You've got red on you.'
        return(jsonify(data))

    
    def home(self):
        """Froggy custom route
        This function renders Froggy's landpage.
        """
        with open(os.path.join(TEMPLATE_FOLDER, "pond.html"), 'r') as file:
            data = file.read()
        # 'I am Groot.'
        return(data)

