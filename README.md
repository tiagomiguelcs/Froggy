# Froggy
![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Flask-97ca00?style=for-the-badge&logo=flask&logoColor=white)
![](https://img.shields.io/badge/Sqlite3-fe814c?style=for-the-badge&logo=sqlite&logoColor=white)
![](https://img.shields.io/badge/apidoc-3776AB?style=for-the-badge&logo=git&logoColor=white)
<p align="center">
  <img width="168px" height="168px" src="https://github.com/tiagomiguelcs/Froggy/blob/master/froggy/static/logo.png"/><br/>
  Froggy - <b>The Python REST Framework</b><br/>
  A keep it simple, stupid (KISS) framework for the development of REST-based services.
</p>


# Installation 
In order to use **<span style="color:#adc03a"> froggy:frog:</span>** on your projects, you can install it with ```pip3```:
```terminal
git clone https://github.com/tiagomiguelcs/froggy.git
cd froggy
pip3 install .
npm install -g apidoc
```
or
```terminal
pip3 install git+https://github.com/tiagomiguelcs/froggy.git
npm install -g apidoc
```

## Documentation
You can find the documentation at the following [link](https://tiagomiguelcs.github.io/froggy/).

# Quick start
A minimal restful API can be implemented using  **<span style="color:#adc03a"> froggy's:frog:</span>** **``Framework``** class. 
```python
# minimal.py
from flask import Flask, request
import froggy
from froggy.framework import Framework

app = Flask(__name__)
framework = Framework(app)

@framework.frogify('/hello_world', methods=['GET'])
def hello_world():
    return 'Hello, World!'
```

```console
export FLASK_APP=minimal.py
flask run
```


# Cookbook
Several 'recipes' for the implementation of REST-based Flask Services using **<span style="color:#adc03a"> Froggy:frog:</span>** can be found below:

- [Using Froggy's Exceptions Handling API](#using-froggys-exceptions-handling-api)
- [Using Froggy's Response Wrapper](#using-froggys-response-wrapper)
- [Using Froggy's Database API](#using-froggys-database-api)
- [Using Froggy's File Handling API](#using-froggys-file-handling-api)
  - [Upload File](#upload-file)
  - [Retrieve File](#retrieve-file)
  - [Retrieve the List of Files](#retrieve-the-list-of-files)
  - [Remove a File](#remove-a-file)
- [Building an Authentication API](#building-an-authentication-api)
  - [Building a Service for Authorized Users](#building-a-service-for-authorized-users)
  - [Building a Service for Authorized Groups](#building-a-service-for-authorized-users)

### Using Froggy's Exceptions Handling API
**<span style="color:#adc03a"> Froggy:frog:</span>** provides an exception handling API that auto returns a response object with details regarding an exception that was raisen.  
```python
# exception.py
import os
from flask import Flask, request
from froggy.framework import Framework
from froggy.exceptions import BadRequest

app         = Flask(__name__)
# The value of key "docs" defines the path where the documentation 
# should be stored by froggy's apiDoc wrapper.
settings    = {"docs": os.getcwd()}
framework   = Framework(app, settings)

@framework.frogify('/divide/<int:x>/<int:y>', methods=['GET'])
def divide(x, y):
    try:
      result =  x / y
      return framework.response(result)
    except Exception as e:
        raise BadRequest(path=request.path, error=str(e))
```

### Using Froggy's Response Wrapper
A response JSON Object can be returned by a service with a single line of code. **<span style="color:#adc03a"> Froggy:frog:</span>** response wrapper uses [Flask's](https://flask.palletsprojects.com/en/1.1.x/api/)  **`make_response`** and **`jsonify`** methods.

```python
# response.py
import os
from flask import Flask, request
from froggy.framework import Framework

app         = Flask(__name__)
# The value of key "docs" defines the path where the documentation 
# should be stored by froggy's apiDoc wrapper.
settings    = {"docs": os.getcwd()}
framework   = Framework(app, settings)

@framework.frogify('/hello/<name>', methods=['GET'])
def hello(name):
    return framework.response("Hello,"+name)
```

### Using Froggy's Database API
You can easly modify data and table structures using **<span style="color:#adc03a"> froggy's:frog:</span>** [SQLite3](https://www.sqlite.org/index.html) - [MySQL](https://www.mysql.com/) is also supported - wrapper that takes care of exceptions, cursor handling, and results formating:
```python
# sqlite3.py
import sqlite3, os
from flask import Flask, request
from froggy.framework import Framework
from froggy.database import Type
from froggy.database import Query

app      = Flask(__name__)
framework = Framework(app)

@framework.frogify('/sqlite3/example', methods=['GET'])
# curl -d "email='kermit@muppets.com&psw=123" -X POST http://localhost:5000/auth/signup
def example():
    conn    = sqlite3.connect('example.db')
    query   = Query(conn, Type.Sqlite3)

    query.execute("CREATE TABLE User (id INTEGER PRIMARY KEY AUTOINCREMENT, email text UNIQUE)")
    query.execute("INSERT INTO User (email) VALUES (?)", ("kermit@muppets.com",))

    """ A dictionary, or a list of dics, will be returned with the 
        resulting data of the SELECT statement for user 'kermit'.
    """
    results = query.execute("SELECT * FROM User")
    conn.close()
    return(framework.response(results))
```
The returned JSON response object:
```json
{
  "froggy": "0.0.1", 
  "status": 200,
  "data": {
    "email": "kermit@muppets.com", 
    "id": 1
  }
}
```
### Using Froggy's File Handling API
Froggy can also help you to build a file handling system by wrapping several ```Flask``` and ```Python.os``` methods to handle files. 

⚠️ **For file handling operations, it is highly recommend to use froggy's built-in authorization system (see [Building a Service for Authorized Users](#building-a-service-for-authorized-users)).**

### Upload File
In order to upload a file a public or static folder must exist on the root of the project. The service to upload a file can be implemented as follows:

```python
# upload_file.py
UPLOAD_DIR = os.path.join(os.getcwd(),"public")

@framework.frogify('/cookbook/files/upload', methods=['POST'])
def upload():
    file = froggy.files.File(request.files['file'], UPLOAD_DIR, {"txt", "md"})
    if file.upload(): return(framework.response())
```

You can test the upload service using the following curl command:
```shell 
curl -X POST --form file=@sample.txt http://localhost:5000/cookbook/files/upload
```

### Retrieve File
The following service can be implemented to retrieve a file from a public or static folder:

```python
# get_file.py
UPLOAD_DIR = os.path.join(os.getcwd(),"public")

@framework.frogify('/cookbook/files/get/<path:filename>', methods=['GET'])
def get_file(filename):
    return(froggy.files.File.get(UPLOAD_DIR, filename, True))
```

### Retrieve the List of Files 
The following service can be implemented to retrieve the list of files available on a public or static folder:

```python
# get_files.py
UPLOAD_DIR = os.path.join(os.getcwd(),"public")

@framework.frogify('/cookbook/files', methods=['GET'])
def get_files(filename):
    return(framework.response(froggy.files.File.list(UPLOAD_DIR)))
```

### Remove a File 
The following service can be implemented to remove a file from a public or static folder:

```python
# remove_file.py
UPLOAD_DIR = os.path.join(os.getcwd(),"public")

@framework.frogify('/cookbook/files/<string:filename>', methods=['DELETE'])
def remove_file(filename):
    if (froggy.files.File.remove(UPLOAD_DIR, filename)): return(framework.response())
```


### Building an Authentication API
An authentication API should include services to signup users, perform server-side authentication and logout procedures. These services can be easly implemented using **<span style="color:#adc03a"> froggy's:frog:</span>** implementations of [JWT](https://jwt.io/) and [SQLite3](https://www.sqlite.org/index.html):

```python
# auth.py
import sqlite3, froggy
from flask import Flask, request
from froggy.framework import Framework
from froggy.authentication import JWTAuth
from froggy.database import Query
from froggy.exceptions import BadRequest

app      = Flask(__name__)
settings = {"authentication": {"type": JWTAuth, "jwt_secret_token": "'Nobody-Calls-Me-Chicken'",
            "jwt_expiration_seconds": 86400}}
framework = Framework(app, settings)

@framework.frogify('/auth/signup', methods=['POST'])
def signup():
    # On a production env do NOT POST your password without SSL enabled.
    email = request.form['email']
    psw   = request.form['psw'] 
    # Hashing the password using the function available on the authentication module.
    hashed_psw  = framework.auth.hash_password(psw)
    conn        = sqlite3.connect('auth.db')
    query       = froggy.database.Query(conn, froggy.database.Type.Sqlite3)
    try:
        query.execute("CREATE TABLE User (id INTEGER PRIMARY KEY AUTOINCREMENT, email text UNIQUE, psw text)")
        query.execute("INSERT INTO User (email, psw) VALUES (?, ?)", (email, hashed_psw))
    except: pass
    conn.close()
    return(framework.response())

@framework.frogify('/auth/login', methods=['POST'])
def do_login():
    # On a production env do NOT POST your password without SSL enabled. 
    email = request.form['email']
    psw   = request.form['psw']  
    conn  = sqlite3.connect('auth.db')
    query = froggy.database.Query(conn, froggy.database.Type.Sqlite3) 
    user  = query.execute("SELECT id, email, psw FROM user WHERE email=?", (email,))
    
    # Raise exception if the user is not found 
    if (not bool(user)):
        raise BadRequest(path=request.path,message="Frog not Found", error="Unknown User", status=403)

    database_stored_hashed_password = user['psw']
    del user['psw'] 

    # Perfom authentication using froggy's authentication API
    framework.auth.authenticate(user, email, database_stored_hashed_password, psw)
    # Return user info, including the JWT.
    return(framework.response(user))

@framework.frogify('/auth/logout', methods=['GET'])
def do_logout():
    # In order to properly logout when calling this service you need to 
    # define the authorization header with the user JWT.
    return(framework.auth.hop_out(request))
```

To test your newly implemented services you can run the following *curl* commands:
```console
curl -d "email='kermit@muppets.com&psw=123" -X POST http://localhost:5000/auth/signup
curl -d "email='kermit@muppets.com&psw=123" -X POST http://localhost:5000/auth/login
curl --request GET http://localhost:5000/auth/logout -H 'Authorization: <Replace-With-User-JWT>'
```
On a production environment, please, **do not post your password without** SSL enabled. 


### Building a Service for Authorized Users
**<span style="color:#adc03a"> Froggy:frog:</span>** can also help you out to implement services that are only accessible by **authorized** users with a valid JWT (i.e., with an active login session):
```python
# secure_user.py
# Only authenticated users can access this service.
from flask import Flask, request
import froggy
from froggy.framework import Framework

app = Flask(__name__)
framework = Framework(app)

@framework.frogify('/auth/fort_knox', authorization=True, methods=['GET'])
def fort_knox():
    return(framework.response(data={"message": "Secure service only accessible by authorized users with a valid JWT."}))
```

This service can be tested using the following *curl* command:
```console
curl -H "Authorization: <Replace-With-User-JWT>" http://localhost:5000/auth/fort_knox
```

### Building a Service for Authorized Groups
**<span style="color:#adc03a"> Froggy:frog:</span>** can also help you out to implement services that are only accessible by **authorized users** with a valid JWT and beloging to a list of **groups**.

```python
# secure_group.py
# Only users that belong to group 1 and/or 2 can access this service.
@framework.frogify('/auth/secure', groups=[1,2], authorization=True, methods=['GET'])
def fort_knox():
    # The user JSON Object encoded in the JWT should contain a list of groups of the user. 
    return(framework.response(data={"message": "this is a secure service only accessible by authorized users."}))

```

### Deploying Documentation
A service can be easly documented using **<span style="color:#adc03a"> froggy's:frog:</span>** [apiDoc](https://github.com/apidoc/apidoc) wrapper.

1. Create a file called [**`apidoc.json`**](https://apidocjs.com/#example-basic) on the root of the project as follows: 
```json
{
    "name": "Documentation Demo",
    "version": "1.0.0",
    "description": "Description.",
    "title": "Demo",
    "sampleUrl": "http://localhost:5000"
}
```
2. Create the main froggy application and add some [API annotations](https://apidocjs.com/#example-basic) to a service:

```python
# main.py
import os
from flask import Flask, request
from froggy.framework import Framework

app         = Flask(__name__)
# The value of key "docs" defines the path where the documentation 
# should be stored by froggy's apiDoc wrapper.
settings    = {"docs": os.getcwd()}
framework   = Framework(app, settings)

@framework.frogify('/hello/<name>', methods=['GET'])
def hello(name):
    """
    @api {get} /hello/:name Hello World
    @apiName demo 
    @apiDescription Example of a simple 'Hello World' service.
    @apiGroup Generic
    @apiParam {String} name Name of the guest.
    @apiSuccess {String} message The Hello World Message. 
    @apiExample {curl} Example usage:
        curl -i http://localhost:5000/hello/Anna
    """
    return framework.response("Hello,"+name)
```
3. You're done:thumbsup:! You can now access the documentation created under the root of the project. 

# Developing Froggy
<!-- Be free to fork away, froggy can be easly developed using the following set of commands -->
Soonish

# Issues

Found a bug or want a new feature ? Please let us know by submitting an issue.
