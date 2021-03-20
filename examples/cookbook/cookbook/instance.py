import froggy
SETTINGS = {
     "name": "cookbook", # Name of the application
     "package": __package__, # Name of this package
     "documentation": True, # Set to true if you want to generate documentation
     "authentication": {
         "type": froggy.authentication.JWTAuth, # Set the default authentication method, i.e., JWT Web Tokens
         "jwt_secret_token": "'Nobody-Calls-Me-Chicken'",
         "jwt_expiration_seconds": 86400
     },
     "logo": True # Set to true if you want to see froggy face on the flask run terminal
}
