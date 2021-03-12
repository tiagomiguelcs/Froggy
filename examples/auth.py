"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-

Froggy Authentication/Authorization Demo Services. 
"""
from froggy import framework
from flask import Flask, request
import time, sqlite3, os
from handlers.hops import frogify
from handlers.exceptions import BadRequest
from handlers.gadgets import print, json_response
from handlers.auth import authenticate, hop_out

@frogify('/examples/auth/login', methods=['POST'])
def login():
    """
    @api {post} /examples/auth/login Authentication Service    
    @apiName demo 
    @apiDescription Example of an Authentication Service using sqlite3 and the froggy framework. 
    @apiGroup User
    @apiParam {String} email=kermit@muppets.com Email of the user.
    @apiParam {String} psw=123 User's password. 
    @apiExample {curl} Example usage:
        curl -d "email=kermit@muppets.com&psw=123" -X POST http://localhost:5000/examples/auth/login
    """
    email = request.form['email']
    psw   = request.form['psw']
    db_psw = None
    try: 
        os.remove('examples/auth.db')
    except:
        pass
    con = sqlite3.connect('examples/auth.db')
    try:
        cur = con.cursor();
        # Create the table that will contain our test user
        cur.execute("CREATE TABLE User (id int, email text UNIQUE, psw text, createdon datetime, updatedon datetime)")
        # Add test user, the default password will be 123 that was previously hashed salted. 
        cur.execute("INSERT INTO User VALUES (1, 'kermit@muppets.com','6e68eff9ad873e8df6d25fce9282fb9bfbd3f8f6ff32a639a42963448787d88a:7e3627579e1e4304874ce442f2e50760', CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)")
        con.commit()
        cur.execute("SELECT id, email, psw FROM User WHERE email=?", [email]);
    except Exception as e:
       raise BadRequest(path=request.path,message="Unable to retrieve user information",error=str(e),status=403)
    
    # Process the database results
    records = cur.fetchall()
    user = {}
    for row in records:
        user['id']      = row[0]
        user['email']   = row[1]
        db_psw          = row[2]
    
    cur.close()
    con.close()

    if (not bool(user)):
        raise BadRequest(path=request.path,message="Frog not Found", error="Unknown User", status=403)

    # Perfom authentication using the predefined framework method
    authenticate(user,user['email'], db_psw, psw)

    # Authentication was a success, the 'frog' 'can follow the white rabbit!".
    return(json_response(user))

@frogify('/examples/auth/logout', methods=['GET'])
def logout():
    """"
    @api {get} /examples/auth/logout Logout Service   
    @apiName logout 
    @apiDescription Server side logout using the JWT token. 
    @apiGroup User
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" http://localhost:5000/examples/auth/logout
    @apiHeader (Authorization) {String} Authorization Web Token
    """
    return(hop_out(request))


@frogify('/examples/auth/secure', authorization=True, methods=['GET'])
def secure():
    """"
    @api {get} /examples/auth/secure Secured Service    
    @apiName secure 
    @apiDescription Autorization Service, the secure service can only be accessed if the user has a valid authorization token issued by froggy. 
    @apiGroup User
    @apiExample {curl} Example usage:
        curl -H "Authorization: <token>" http://localhost:5000/examples/auth/secure
    @apiHeader (Authorization) {String} Authorization Web Token
    """
    return(json_response(data={"message": "this is a secure service only accessible by authorized users."}))
