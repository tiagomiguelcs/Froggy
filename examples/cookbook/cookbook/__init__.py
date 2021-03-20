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
from froggy.gadgets import normpath
from cookbook.instance import SETTINGS

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
    try:
        con = sqlite3.connect('cookbook.db')
        cur = con.cursor()
        # Create the database structure 
        cur.execute("CREATE TABLE User (id INTEGER NOT NULL PRIMARY KEY, email text UNIQUE, psw text, createdon datetime, updatedon datetime)")
        cur.execute("CREATE TABLE My_Group (id INTEGER NOT NULL PRIMARY KEY, name text, createdon datetime, updatedon datetime)")
        cur.execute("CREATE Table User_Group (user_id INTEGER NOT NULL, group_id INTEGER NOT NULL, createdon datetime, updatedon datetime,PRIMARY KEY (user_id, group_id), FOREIGN KEY (user_id) REFERENCES User(id), FOREIGN KEY (group_id) REFERENCES My_Group(id))")
        con.commit()
        # Create sample content
        cur.execute("INSERT INTO User VALUES (1, 'kermit@muppets.com','6e68eff9ad873e8df6d25fce9282fb9bfbd3f8f6ff32a639a42963448787d88a:7e3627579e1e4304874ce442f2e50760', CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)")
        cur.execute("INSERT INTO My_Group VALUES (1, 'user', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
        cur.execute("INSERT INTO My_Group VALUES (2, 'admin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
        # Kermit will be part of user group 'user'
        cur.execute("INSERT INTO User_Group VALUES (1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
        cur.execute("CREATE VIEW Users_View AS SELECT User.id as user_id, My_Group.id as group_id, My_Group.name as group_name, User.email, User.psw, My_Group.createdon, My_Group.updatedon FROM User, My_Group, User_Group WHERE User.id = User_Group.user_id AND My_Group.id = User_Group.group_id")
        con.commit()
        return(con)
    except Exception as e:
        raise framework.BadRequest(path=request.path,message=str(e), error="Database", status=500)

@framework.frogify('/', methods=['GET'])
def documentation():
    """Demo Documentation 
    
    'Welcome to the Cafe 80's, where it's always morning in America, even in the afternoo-noo-noon. Our special today is mesquite-grilled sushi.'
    """
    return app.send_static_file('index.html')

@framework.frogify('/cookbook/auth/login', methods=['POST'])
def do_login():
    """
    @api {post} /cookbook/auth/login Login Example    
    @apiName authenticate 
    @apiDescription Example of an Authentication Service using sqlite3 and the froggy framework. 
    @apiGroup Guest
    @apiParam {String} email=kermit@muppets.com Email of the user.
    @apiParam {String} psw=123 User's password. 
    @apiExample {curl} Example usage:
        curl -d "email=kermit@muppets.com&psw=123" -X POST http://localhost:5000/cookbook/auth/login
    """
    email = request.form['email']
    psw   = request.form['psw']
    db_psw = None
    # Let's create the database schema
    con = create_database()
    try:
        cur = con.cursor();
        cur.execute("SELECT id, email, psw, createdon, updatedon FROM User WHERE email=?", [email]);
    except Exception as e:
       raise BadRequest(framework, path=request.path,message="Unable to retrieve user information",error=str(e),status=403)
    
    # Process the database results
    records = cur.fetchall()
    user = {}
    for row in records:
        user['id']          = row[0]
        user['email']       = row[1]
        user['createdon']   = row[3]
        user['updatedon']   = row[4]
        db_psw              = row[2]

    # Let's get each group the user belongs 2
    try:
        cur.execute("SELECT group_id, group_name, createdon, updatedon FROM Users_View WHERE user_id=?", [user['id']])
    except Exception as e:
       raise BadRequest(framework, path=request.path,message="Unable to retrieve user information",error=str(e),status=403)
    user['groups'] = [] 
    for row in cur.fetchall():
        group = {}
        group['id']         = row[0]
        group['name']       = row[1]
        group['createdon']  = row[2]
        group['updatedon']  = row[3]
        user['groups'].append(group)
    
    cur.close()
    con.close()

    if (not bool(user)):
        raise BadRequest(framework, path=request.path,message="Frog not Found", error="Unknown User", status=403)
    
    # Perfom authentication using the predefined framework method
    framework.auth.authenticate(user, user['email'], db_psw, psw)
    # Authentication was a success, the 'frog' 'can follow the white rabbit!".
    return(framework.response(user))

@framework.frogify('/cookbook/auth/logout', methods=['GET'])
def do_logout():
    """"
    @api {get} /cookbook/auth/logout Logout Example   
    @apiName logout 
    @apiDescription Server side logout using the JWT token. 
    @apiGroup User
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" http://localhost:5000/cookbook/auth/logout
    @apiHeader (Authorization) {String} Authorization Web Token
    """
    return(framework.auth.hop_out(request))

@framework.frogify('/cookbook/auth/secure', groups=[1,2], authorization=True, methods=['GET'])
def do_secure():
    """"
    @api {get} /cookbook/auth/secure Secured Service Example
    @apiName secure 
    @apiDescription Autorization Service, the secure service can only be accessed if the user has a valid authorization issued by froggy. 
    @apiGroup User
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" http://localhost:5000/cookbook/auth/secure
    @apiHeader (Authorization) {String} Authorization Web Token
    """
    return(framework.response(data={"message": "this is a secure service only accessible by authorized users."}))

@framework.frogify('/cookbook/hello_world/<name>', authorization=False, methods=['GET'])
def demo(name):
    """
    @api {get} /cookbook/hello_world/:name Hello World Example
    @apiName demo 
    @apiGroup Guest
    @apiParam {String} name Name of the guest.
    @apiSuccess {String} message The Hello World Message. 
    @apiExample {curl} Example usage:
        curl -i http://localhost:5000/cookbook/hello_world/Anna
    """
    data={"message": "Hello World, "+name}
    return framework.response(data)
