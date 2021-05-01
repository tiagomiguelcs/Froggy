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
        # Create sample content
        con = sqlite3.connect('cookbook.db')
        cur = con.cursor()
        # Create the database structure 
        cur.execute("CREATE TABLE User (id INTEGER NOT NULL PRIMARY KEY, email text UNIQUE, psw text, createdon datetime, updatedon datetime)")
        cur.execute("CREATE TABLE My_Group (id INTEGER NOT NULL PRIMARY KEY, name text, createdon datetime, updatedon datetime)")
        cur.execute("CREATE Table User_Group (user_id INTEGER NOT NULL, group_id INTEGER NOT NULL, createdon datetime, updatedon datetime,PRIMARY KEY (user_id, group_id), FOREIGN KEY (user_id) REFERENCES User(id), FOREIGN KEY (group_id) REFERENCES My_Group(id))")
        con.commit()
        
        # Let's create a hashed password for user 'kermit'
        password   = "123"
        # You can hash the password using the function available on the authentication module.
        hashed_psw = framework.auth.hash_password(password)
        # print("hashed_psw" + str(hashed_psw))        

        cur.execute("INSERT INTO User VALUES (1, 'kermit@muppets.com',?, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)", [hashed_psw])
        cur.execute("INSERT INTO My_Group VALUES (1, 'user', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
        cur.execute("INSERT INTO My_Group VALUES (2, 'admin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
        # Kermit will be part of user group 'user'
        cur.execute("INSERT INTO User_Group VALUES (1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
        cur.execute("CREATE VIEW Users_View AS SELECT User.id as user_id, My_Group.id as group_id, My_Group.name as group_name, User.email, User.psw, My_Group.createdon, My_Group.updatedon FROM User, My_Group, User_Group WHERE User.id = User_Group.user_id AND My_Group.id = User_Group.group_id")
        con.commit()
        return(con)
    except Exception as e:
        raise BadRequest(path=request.path,message=str(e), error="Database", status=500)

@framework.frogify('/', methods=['GET'])
def documentation():
    """Demo Documentation 
    
    'Welcome to the Cafe 80's, where it's always morning in America, even in the afternoo-noo-noon. Our special today is mesquite-grilled sushi.'
    """
    return app.send_static_file('index.html')

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

@framework.frogify('/cookbook/databases/sqlite3/<statement>')
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
        conn        = sqlite3.connect('cookbook.db')
    else:
        conn        = create_database()

    database    = froggy.database.SQL(conn, Type.Sqlite3)   
    # SQLite3 SELECT Example
    if (operation == "select"):
        sql         = "SELECT * FROM user"
        return(framework.response(database.select(sql)))
    
    # SQLite3 INSERT Example
    if (operation == "insert"):
        last_id     = database.get_last_id("user", "id")
        sql         = "INSERT INTO user (id, email) VALUES (?, ?)"
        data        = (last_id+1, 'mr_toad_n'+str(last_id+1)+'@pond.com')
        return (framework.response(database.insert(sql, data)))

    # SQLite3 UPDATE Example
    if (operation == "update"):
        sql         = "UPDATE user SET email=? WHERE id=?"
        data        = ('mr_toad_updated@pond.com', 2)
        database.update(sql, data)
        return (framework.response(status=200))
    
    # SQLite3 UPDATE Example
    if (operation == "delete"):
        sql         = "DELETE FROM user WHERE id>?"
        data        = (1,)
        database.delete(sql, data)
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

    
    # MySQL SELECT Example
    if (operation == "select"):
        sql         = "SELECT * FROM user"
        return(framework.response(database.select(sql)))
    
    # MySQL UPDATE Example
    if (operation == "insert"):
        last_id     = database.get_last_id("user", "id")
        sql         = "INSERT INTO user (id, email, psw) VALUES (%s, %s, %s)"
        data        = (last_id+1, 'mr_toad_n'+str(last_id+1)+'@pond.com', 'test')
        database.insert(sql, data)

    # MySQL UPDATE Example
    if (operation == "update"):
        sql         = "UPDATE user SET email=%s WHERE id=%s"
        data        = ('mr_toad_updated@pond.com', 2)
        database.update(sql, data)
    
    # MySQL UPDATE Example
    if (operation == "delete"):
        sql         = "DELETE FROM user WHERE id>%s"
        data        = (1,)
        database.delete(sql, data)

    '''