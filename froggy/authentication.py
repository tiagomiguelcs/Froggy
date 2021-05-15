""""""
"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
Froggy Authentication
"""
from flask import request
from datetime import datetime, timedelta
import sqlite3, os, hashlib, jwt, dateparser, codecs, bcrypt
import froggy

class Authentication(froggy.framework.Framework):
    """The main Authentication class. This class is parent of several sub authentication classes  :class:`froggy.Authentication.JWTAuth`."""
    def __init__(self):
        pass
    
    def check_password(self, db_hashed_psw, user_psw):
        """Check if a hashed password (from a database) is equal to the one provided by a user.

        :param db_hashed_psw: The hashed password.
        :type db_hashed_psw: bytes
        :param user_psw: The plaintext user inputted password.
        :type user_psw: str
        :return: True if both passwords are equal, false otherwise.
        :rtype: bool
        """
        if bcrypt.checkpw(user_psw.encode(), db_hashed_psw):
            # 'This is Sparta!'
            return(True)
        else:
            # 'I'm walking here! I'm walking here!'
            return(False)
    
    def hash_password(self, psw):
        """ Hash a password with some 'salt' using bcrypt

        :param psw: The password to hash.
        :type psw: str
        :return: The hashed password that includes the 'salt'.
        :rtype: str
        """
        salt = bcrypt.gensalt()
        hashed_psw = bcrypt.hashpw(psw.encode(), salt)
        return(hashed_psw)


class JWTAuth(Authentication):
    """ Authentication class based on JWT. The authentication and authorization implementations follows the workflow defined for JSON Web Tokens (JWT), see https://jwt.io/introduction for more details.
    """  
    def __init__(self, JWT_SECRET_TOKEN, JWT_EXPIRATION_SECONDS):
        """JWTAuth Class Constructor.

        :param JWT_SECRET_TOKEN: The JWT Secret Token.
        :type JWT_SECRET_TOKEN: str
        :param JWT_EXPIRATION_SECONDS: JWT expiration time in seconds.
        :type JWT_EXPIRATION_SECONDS: int
        """
        super().__init__()
        self.JWT_EXPIRATION_SECONDS = JWT_EXPIRATION_SECONDS
        self.JWT_SECRET_TOKEN       = JWT_SECRET_TOKEN

    def authenticate(self, user, email, db_psw, psw):
        """Authenticates the user by comparing two hashed and dynamically salted passwords. The access token will be store on the provide user dic.

        :param user: The user is represented as a Python dictionary and it will be included in the authorization access token.
        :type user: dict
        :param email: User email.
        :type email: str
        :param db_psw: Database password (salted and hashed).
        :type db_psw: str
        :param psw:  Plaintext password inputted by the user.
        :type psw: str
        :raises froggy.exceptions.BadRequest: Exception on Authentication failure or User already Authenticated.
        """        

        # Check if the hashed password, available on a database, is the same as the one provided by the user.
        if self.check_password(db_psw, psw):
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
            user['exp']     = datetime.utcnow() + timedelta(seconds=int(self.JWT_EXPIRATION_SECONDS))
            user['token']   = (jwt.encode(user, self.JWT_SECRET_TOKEN, algorithm='HS256'))
            
            # Insert the access token into the auth table
            try:
                cur.execute("INSERT INTO auth VALUES (?,?,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",[user['token'], email])
                con.commit()
            except sqlite3.IntegrityError as e:
                raise froggy.exceptions.BadRequest(path=request.path, error=str(e), message="User Already Authenticated with token="+user['token'], status=200)
            
            # Just close an 'go home'.
            cur.close()
            con.close()
        else:
            # Frog MIA
            raise froggy.exceptions.BadRequest(path=request.path,message="Unknown Frog",error="Authentication failure",status=401,debug=True)

    def hop_out(self, request):
        """Log out using the authorization access token provided by the user in the header of the request.

        :param request: The current request object.
        :type request: Request Object
        :raises froggy.exceptions.BadRequest: For database related errors.
        :return: Returns a json response object.
        :rtype: Response Object
        """
        con     = sqlite3.connect(".froggy.db")
        cur     = con.cursor()
        token   = self.get_auth_token(request)
        # Remove the authorization token from the database, i.e., user will no longer be able to use froggy's services.
        try:
            cur.execute("DELETE FROM auth WHERE token=?",[token])      
            con.commit()
        except sqlite3.Error as e:
            cur.close()
            con.close()
            raise froggy.exceptions.BadRequest(path=request.path,message=(str(e.args)),error="SQlite3 Error",status=500)
        cur.close()
        con.close()
        # "'I have to return some videotapes'"
        return self.response()

    def get_auth_token(self, request):
        """Retrieve the authorization token from the request header.

        :param request: The current request object.
        :type request: Request object
        :raises froggy.exceptions.BadRequest: When an authorization token was not provided.
        :return: Returns the authorization access token.
        :rtype: str
        """
        headers = dict(request.headers)
        if 'Authorization' not in headers: 
            # Authentication token MIA raise bad request
            raise froggy.exceptions.BadRequest(path=request.path,message="Authorization token not provided",error="Authorization Failure",status=403)
        # 'You're a wizard, 'arry.'"
        return (headers['Authorization'])

    def expired_or_invalid(self, token):
        """Check if a token is still valid (expired?).

        :param token: The authorization access token of the user.
        :type token: str
        :return: True if the token is expired, false otherwise.
        :rtype: bool
        """
        # Let's just use jwt.decode to verify if the token is expired or invalid
        try:
            jwt.decode(token, self.JWT_SECRET_TOKEN, algorithms=['HS256'])
            # 'Just keep swimming'"
            return False
        except (jwt.DecodeError, jwt.ExpiredSignatureError) as e: 
            # 'I volunteer as tribute.'
            return True
            #raise BadRequest(path=request.path, message="Authorization token expired", error=str(e) )

    def in_group(self, request, allowed_groups):
        """Check if user is in a group allowed to access the target resource.

        :param request: The current request object.
        :type request: Request object
        :param allowed_groups: The list of groups (IDs) that are allowed to access a target resource.
        :type allowed_groups: list
        :return: True if the user belongs to the set of groups allowed to access a target resource, false otherwise.
        :rtype: bool
        """
        token = self.get_auth_token(request)
        user = jwt.decode(token, self.JWT_SECRET_TOKEN, algorithms=['HS256'])

        for user_group in user['groups']:
            for group in allowed_groups: 
                if user_group['id'] == group: 
                    # 'With great power comes great responsability'
                    return True
        # 'You will ride eternal, shiny and chrome.'
        return False

    def authorized(self, request):
        """Check if the user is authenticated, authorized to access a service. The authorization procedure is accomplished by checking if the authorization token of the user is available on the database.

        :param request: The request object.
        :type request: Request object
        :return: Returns true if the user is authorized to access a resource, false otherwise.
        :rtype: bool
        """
        # Check if an authentication token is available on the request header
        token = self.get_auth_token(request)

        # fprint("Searching for token: " + str(token))
        # Check if the token exists on the database, table auth
        con = sqlite3.connect(".froggy.db")
        cur = con.cursor()
        
        # Get the list of registered tokens
        for row in cur.execute("SELECT token FROM auth WHERE token=?",[token]):
            # Check if the authorization token is still valid (i.e., is the token expired ?)
            if (self.expired_or_invalid(token)):
                # If the token is expired or invalid, remove the authorization from the database and return false 
                # that is, the user is no longer authorized to access the requested resource.
                cur.execute("DELETE FROM auth WHERE token=?", [token])
                con.commit()
                # 'Not the bees!'
                return(False)
            cur.close()
            con.close()
            # 'Are you watching closely?'
            return(True)
        
        cur.close()
        con.close()
        # 'I was perfect.'
        return(False)
