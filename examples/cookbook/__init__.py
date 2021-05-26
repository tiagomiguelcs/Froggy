"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's Code Examples
"""
from flask import Flask, request
import os, sqlite3, froggy
from froggy.framework import Framework
from froggy.exceptions import BadRequest
from froggy.gadgets import normpath, exists
from froggy.database import Type

SETTINGS = {
     "name": "cookbook", # Name of the application
     "docs": os.getcwd(),
     "authentication": {
         "type": froggy.authentication.JWTAuth, # Set the default authentication method, i.e., JWT Web Tokens
         "jwt_secret_token": "'Nobody-Calls-Me-Chicken'",
         "jwt_expiration_seconds": 86400
     },
}
UPLOAD_DIR = os.path.join(os.getcwd(),"public")

# Instanciate the Flask class and froggy framework initialized with the Flask application.
app = Flask(__name__, template_folder='templates', static_url_path="", static_folder="../docs/")
framework = Framework(app, SETTINGS)

def create_database():
    """Create a SQLite3 database

    This function creates a test database to demonstrate the authentication and authorization functionalities of the froggy framework.
    
    Raises:
        framework.BadRequest: [description]
    """
    try:
        os.remove('cookbook.db')
    except:
        pass
    
    # Create sample content
    conn = sqlite3.connect('cookbook.db')    
    query = froggy.database.Query(conn, Type.Sqlite3) 
    
    # Create the database structure 
    query.execute("CREATE TABLE User (id INTEGER PRIMARY KEY AUTOINCREMENT, email text UNIQUE, psw text, createdon datetime, updatedon datetime)")
    query.execute("CREATE TABLE My_Group (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, createdon datetime, updatedon datetime)")
    query.execute("CREATE Table User_Group (user_id INTEGER NOT NULL, group_id INTEGER NOT NULL, createdon datetime, updatedon datetime,PRIMARY KEY (user_id, group_id), FOREIGN KEY (user_id) REFERENCES User(id), FOREIGN KEY (group_id) REFERENCES My_Group(id))")
        
    # Let's create a hashed password for user 'kermit'
    password   = "123"
    # You can hash the password using the function available on the authentication module.
    hashed_psw = framework.auth.hash_password(password)

    query.execute("INSERT INTO User VALUES (?,?,?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", [1, 'kermit@muppets.com', hashed_psw])
    query.execute("INSERT INTO My_Group VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", [1, 'user'])
    query.execute("INSERT INTO My_Group VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", [2, 'admin'])
    # Kermit will be part of user group 'user'
    query.execute("INSERT INTO User_Group VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", [1,1] )
    query.execute("CREATE VIEW Users_View AS SELECT User.id as user_id, My_Group.id as group_id, My_Group.name as group_name, User.email, User.psw, My_Group.createdon, My_Group.updatedon FROM User, My_Group, User_Group WHERE User.id = User_Group.user_id AND My_Group.id = User_Group.group_id")
    
    return(conn)

@framework.frogify('/', methods=['GET'])
def documentation():
    """Demo Documentation 
    
    'Welcome to the Cafe 80's, where it's always morning in America, even in the afternoo-noo-noon. Our special today is mesquite-grilled sushi.'
    """
    return app.send_static_file('index.html')

@framework.frogify('/cookbook/auth/signup', methods=['POST'])
def signup():
    """
    @api {post} /cookbook/auth/signup User Signup    
    @apiName signup 
    @apiDescription Example of an authentication service using sqlite3 and the froggy framework. 
    @apiGroup Authentication
    @apiParam {String} email Email of the user.
    @apiParam {String} psw Desired password.  
    @apiExample {curl} Example usage:
        curl -d "email=frogger@atari.com&psw=123456" -X POST http://localhost:5000/cookbook/auth/signup
    """
    # On a production env do NOT POST your password without SSL enabled.
    email = request.form['email']
    psw   = request.form['psw'] 

    if os.path.exists('cookbook.db'):
        conn    = sqlite3.connect('cookbook.db')
    else:
        conn    = create_database()

    query     = froggy.database.Query(conn, Type.Sqlite3) 
    # Hashing the password using the function available on the authentication module.
    hashed_psw  = framework.auth.hash_password(psw)
    query       = froggy.database.Query(conn, froggy.database.Type.Sqlite3)
    try:
        query.execute("INSERT INTO User (email, psw, createdon, updatedon) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", (email, hashed_psw))
    except: pass
    conn.close()
    return(framework.response())

@framework.frogify('/cookbook/auth/login', methods=['POST'])
def do_login():
    """
    @api {post} /cookbook/auth/login User Login    
    @apiName authenticate 
    @apiDescription Example of an authentication service using sqlite3 and the froggy framework. 
    @apiGroup Authentication
    @apiParam {String} email=kermit@muppets.com Email of the user.
    @apiParam {String} psw=123 User's password. 
    @apiExample {curl} Example usage:
        curl -d "email=kermit@muppets.com&psw=123" -X POST http://localhost:5000/cookbook/auth/login
    """
    # On a production env do NOT POST your password without SSL enabled.
    email = request.form['email']
    psw   = request.form['psw']
    
    # Let's create the database schema
    conn   = create_database()
    query = froggy.database.Query(conn, Type.Sqlite3) 
    
    user    = query.execute("SELECT id, email, psw, createdon, updatedon FROM User WHERE email=?", [email]);
    # Let's get the groups the user belongs 2. The groups of the user should be placed in a list of dics or froggy's group authorization API will not work.
    user['groups'] = []
    user['groups'].append(query.execute("SELECT group_id as id, group_name, createdon, updatedon FROM Users_View WHERE user_id=?", [user['id']]))
    conn.close()

    if (not bool(user)):
        raise BadRequest(path=request.path,message="Frog not Found", error="Unknown User", status=403)
    
    # Perfom authentication using the predefined framework method
    db_psw = user['psw']
    del user['psw']
    framework.auth.authenticate(user, user['email'], db_psw, psw)
    # Authentication was a success, the 'frog' 'can follow the white rabbit!".
    return(framework.response(user))

@framework.frogify('/cookbook/auth/logout', methods=['GET'])
def do_logout():
    """"
    @api {get} /cookbook/auth/logout User Logout   
    @apiName logout 
    @apiDescription Example of a server side logout service that uses previously issued JWT tokens to logout an authenticated user. 
    @apiGroup Authentication
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" http://localhost:5000/cookbook/auth/logout
    @apiHeader (Authorization) {String} Authorization Web Token
    """
    return(framework.auth.hop_out(request))

@framework.frogify('/cookbook/auth/secure', groups=[1,2], authorization=True, methods=['GET'])
def do_secure():
    """"
    @api {get} /cookbook/auth/secure Secure Service
    @apiName secure 
    @apiDescription Example of a secure service that can only be accessed if the user has a valid authorization token issued by froggy. 
    @apiGroup Authentication
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" http://localhost:5000/cookbook/auth/secure
    @apiHeader (Authorization) {String} Authorization Web Token
    """
    return(framework.response(data={"message": "this is a secure service only accessible by authorized users."}))

@framework.frogify('/cookbook/hello_world/<name>', authorization=False, methods=['GET'])
def hello_world(name):
    """
    @api {get} /cookbook/hello_world/:name Hello World
    @apiName demo 
    @apiDescription Example of a simple 'Hello World' service.
    @apiGroup Generic
    @apiParam {String} name Name of the guest.
    @apiSuccess {String} message The Hello World Message. 
    @apiExample {curl} Example usage:
        curl -i http://localhost:5000/cookbook/hello_world/Anna
    """
    data={"message": "Hello Frogs of the World, "+name}
    return framework.response(data)

@framework.frogify('/cookbook/databases/sqlite3/<statement>', methods=['GET'])
def database(statement):
    # : <br/> SELECT * FROM user; <br/> INSERT INTO user (id, email) VALUES (?, ?); <br/> UPDATE user SET email=? WHERE id=?; <br/> DELETE FROM user WHERE id>?;
    """
    @api {get} /cookbook/databases/sqlite3/:statement Data Manipulation
    @apiDescription Example of a service that implements and executes several SQL statements for data manipulation using froggy's database API.
    @apiName database
    @apiGroup Databases
    @apiParam {String} statement Select a sql statement (SELECT, INSERT, UPDATE, or DELETE)
    @apiSuccess {String} Returns the result of the selected SQL statement. 
    @apiExample {curl} Example usage:
        curl -i http://localhost:5000/cookbook/databases/sqlite3/SELECT
    """

    operation = str(statement).lower()

    if os.path.exists('cookbook.db'):
        conn    = sqlite3.connect('cookbook.db')
    else:
        conn    = create_database()

    query     = froggy.database.Query(conn, Type.Sqlite3)   
    # SQLite3 SELECT Example
    if (operation == "select"):
        sql         = "SELECT id,email FROM user"
        return(framework.response(query.execute(sql)))
    
    # SQLite3 INSERT Example
    if (operation == "insert"):
        last_id     = query.get_last_id("user", "id")
        sql         = "INSERT INTO user (id, email) VALUES (?, ?)"
        args        = [last_id+1, 'mr_toad_n'+str(last_id+1)+'@pond.com']
        return (framework.response(query.execute(sql, args)))

    # SQLite3 UPDATE Example
    if (operation == "update"):
        sql         = "UPDATE user SET email=? WHERE id=?"
        args        = ['mr_toad_updated@pond.com', 2]
        query.execute(sql, args)
        return (framework.response(status=200))
    
    # SQLite3 UPDATE Example
    if (operation == "delete"):
        sql         = "DELETE FROM user WHERE id>?"
        args        = [1,]
        query.execute(sql, args)
        return (framework.response(status=200))

    # Not implemented
    return (framework.response(status=501))

    ''' ### MySQL Examples ###
    # Be sure to set the cursor as DictCursor or 
      Froggy's database API will not work properly.
    
    from flaskext.mysql import MySQL
    from pymysql.cursors import DictCursor

    mysql = MySQL(cursorclass=DictCursor) 
    app.config['MYSQL_DATABASE_USER'] = "root"
    app.config['MYSQL_DATABASE_PASSWORD'] = "your_password"
    app.config['MYSQL_DATABASE_DB'] = "demo"
    app.config['MYSQL_DATABASE_HOST'] = "localhost"
    mysql.init_app(app)

    operation = str(statement).lower()
    database  = froggy.database.Query(conn, Type.Sqlite3) 

    # MySQL SELECT Example
    if (operation == "select"):
        sql         = "SELECT * FROM user"
        return(framework.response(database.execute(sql)))
    
    # MySQL UPDATE Example
    if (operation == "insert"):
        last_id     = database.get_last_id("user", "id")
        sql         = "INSERT INTO user (id, email, psw) VALUES (%s, %s, %s)"
        args        = [last_id+1, 'mr_toad_n'+str(last_id+1)+'@pond.com', 'test']
        database.execute(sql, args)

    # MySQL UPDATE Example
    if (operation == "update"):
        sql         = "UPDATE user SET email=%s WHERE id=%s"
        args        = ['mr_toad_updated@pond.com', 2]
        database.execute(sql, args)
    
    # MySQL UPDATE Example
    if (operation == "delete"):
        sql         = "DELETE FROM user WHERE id>%s"
        args        = [1,]
        database.execute(sql, args)

    '''

@framework.frogify('/cookbook/files/<string:filename>', authorization=True, methods=['DELETE'])
def remove_file(filename):
    """
    @api {delete} /cookbook/files/hello.txt Remove File
    @apiDescription Example of a service that implements a way to delete a file from a static folder on the server.
    @apiName remove
    @apiGroup File Handling
    @apiHeader (Authorization) {String} Authorization Web Token
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" -X DELETE http://localhost:5000/cookbook/files/sample.txt
    """
    if (froggy.files.File.remove(UPLOAD_DIR, filename)):
        return(framework.response())

@framework.frogify('/cookbook/files', authorization=True, methods=['GET'])
def get_files():
    """
    @api {get} /cookbook/files List Files
    @apiDescription Example of a service that implements a way to return the list of files available on a static folder of the server.
    @apiName list
    @apiGroup File Handling
    @apiHeader (Authorization) {String} Authorization Web Token
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" http://localhost:5000/cookbook/files
    """
    return(framework.response(froggy.files.File.list(UPLOAD_DIR)))

@framework.frogify('/cookbook/files/get/<path:filename>', authorization=True, methods=['GET'])
def get_file(filename):
    """
    @api {get} /cookbook/files/get/sample.txt Get File
    @apiDescription Example of a service that implements a way to download a file from a server static folder.
    @apiName Get
    @apiGroup File Handling
    @apiHeader (Authorization) {String} Authorization Web Token
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" http://localhost:5000/cookbook/files/get/sample.txt
    """
    return(froggy.files.File.get(UPLOAD_DIR, filename, True))

@framework.frogify('/cookbook/files/upload', authorization=True, methods=['POST'])
def upload():
    """
    @api {post} /cookbook/files/upload Upload File
    @apiDescription Example of a service that enables the user to upload a file to a server static folder.
    @apiName Upload
    @apiGroup File Handling
    @apiSampleRequest off
    @apiHeader (Authorization) {String} Authorization Web Token
    @apiSuccess {String} Returns the result of the upload operation.
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" -X POST --form file=@sample.txt http://localhost:5000/cookbook/files/upload
    """
    file = froggy.files.File(request.files['file'], UPLOAD_DIR, {"txt", "md"})
    if file.upload():
        return(framework.response())
    else:
        return(framework.response(status=500))