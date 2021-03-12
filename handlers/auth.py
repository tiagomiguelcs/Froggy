"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-

Froggy Authentication
- Froggy's authentication and authorization implementations follows the workflow defined 
  for JSON Web Tokens (JWT), see https://jwt.io/introduction for more details.
"""

from froggy import framework, __version__, JWT_SECRET_TOKEN, JWT_EXPIRATION_SECONDS
from flask import Flask, request
from datetime import datetime, timedelta
from handlers.exceptions import BadRequest
from handlers.gadgets import print, json_response
import codecs, os, hashlib, jwt, sqlite3, dateparser

def check_password(db_hashed_psw, user_psw):
    """Check if a hashed password (from a database) is equal to the one provided by a user.

    Args:
        db_hashed_psw: hashed password.
        user_psw: plaintext user inputted password. user inputted password (plaintext).
    
    Returns:
        True if both passwords are equal, false otherwise.
    """
    # Split the hash of the password and the salt
    psw, salt = db_hashed_psw.split(':');
    # Hash and salt the password provided by the user, 'psw', and compare it to 'hashed_psw'
    return psw == hashlib.sha256(salt.encode() + user_psw.encode()).hexdigest()

def authenticate(user, email, db_psw, psw):
    """ Authenticates the user by comparing two hashed and dynamically salted passwords.

    Args:
        user    : The user is represented as a Python dictionary and it will be included in the
                  authorization access token.
        email   : User email
        db_psw  : database password (salted and hashed).
        psw     : Plaintext password inputted by the user (sent through https).
    
    Returns:
        Returns an user access token or an exception is raised if the current user was not authenticated.
    """
    # Check if the hashed password, available on a database, is the same as the one provided by the user.
    if check_password(db_psw, psw):
        con = sqlite3.connect(".froggy.db")
        cur = con.cursor()
       
        # Add the access token to a table of an internal froggy database, remove this authorization token after logout or the expiration time is reached.
        try:
            # Only one authorization access token is allowed per user.
            cur.execute("CREATE TABLE auth (token text UNIQUE, email text UNIQUE, createdon datetime, updatedon datetime)")
        except:
            # Assuming the table already exists
            pass

        # Check if user is already authenticated, if so, just create a new token and delete the old one
        cur.execute("SELECT token FROM auth WHERE email=?",[email])
        row = cur.fetchone()
        if row is not None:
            cur.execute("DELETE FROM auth WHERE token=?", [row[0]])
            con.commit()        
        
        # Generate the access token to encode the user data 
        user['exp']     = datetime.utcnow() + timedelta(seconds=int(JWT_EXPIRATION_SECONDS))
        user['token']   = (jwt.encode(user, JWT_SECRET_TOKEN, algorithm='HS256'))
 
        # Insert the access token into the auth table
        try:
            cur.execute("INSERT INTO auth VALUES (?,?,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",[user['token'], email])
            con.commit()
        except sqlite3.IntegrityError as e:
            raise BadRequest(path=request.path, error=str(e), message="User Already Authenticated with token="+user['token'], status=200)
        
        # Just close an 'go home'.
        cur.close()
        con.close()
    else:
        # Frog MIA
        raise BadRequest(path=request.path,message="Unknown Frog",error="Authentication failure",status=401,debug=True)

def hop_out(request):
    """Log out using the authorization access token provided by the user in the header of the request.

    Args:
        request: The current request object.
    
    Returns:
        Returns a json response object.
    """
    con     = sqlite3.connect(".froggy.db")
    cur     = con.cursor()
    token   = get_auth_token(request)
    # Remove the authorization token from the database, i.e., user will no longer be able to use froggy's services.
    try:
        cur.execute("DELETE FROM auth WHERE token=?",[token])      
        con.commit()
    except sqlite3.Error as e:
        cur.close()
        con.close()
        raise BadRequest(path=request.path,message=(str(e.args)),error="SQlite3 Error",status=500)
    cur.close()
    con.close()
    return json_response()

def get_auth_token(request):
    """Get the  authorization token from the request headers.

    Args:
        request: The current request object.

    Returns:
        Returns the authorization access token.
    """
    headers = dict(request.headers)
    if 'Authorization' not in headers: 
        # Authentication token MIA raise bad request
        raise BadRequest(path=request.path,message="Authorization token not provided",error="Authorization Failure",status=403)
    
    return (headers['Authorization'])

def expired_or_invalid(token):
    """Check if a token is still valid (expired?).

    Args:
        token: The authorization access token of the user.
    
    Returns:
        True if the token is expired, false otherwise.
    """
    # Let's just use jwt.decode to verify if the token is expired or invalid
    try:
        jwt.decode(token, JWT_SECRET_TOKEN, algorithms=['HS256'])
        return False
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as e: 
        return True
        #raise BadRequest(path=request.path, message="Authorization token expired", error=str(e) )


def authorized(request):
    """Check if the user is authenticated, authorized to access a service. This is accomplished by checking if the 
    authorization token is available on the database.

    Args:
        request: The current request object.
    
    Returns:
        True if the user is authorized to access a resource, False otherwise.
    """
    # Check if an authentication token is available on the request header
    token = get_auth_token(request)

    # print("Searching for token: " + str(token))
    # Check if the token exists on the database, table auth
    con = sqlite3.connect(".froggy.db")
    cur = con.cursor()
    
    # Get the list of registered tokens
    for row in cur.execute("SELECT token FROM auth WHERE token=?",[token]):
        # Check if the authorization token is still valid (i.e., is the token expired ?)
        if (expired_or_invalid(token)):
            # If the token is expired or invalid, remove the authorization from the database and return false 
            # that is, the user is no longer authorized to access the requested resource.
            cur.execute("DELETE FROM auth WHERE token=?", [token])
            con.commit()
            return(False)
        cur.close()
        con.close()
        return(True)
    
    cur.close()
    con.close()
    return(False)
