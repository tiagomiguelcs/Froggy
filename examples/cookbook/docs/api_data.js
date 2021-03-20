define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "/home/tiagomiguelcs/SynologyDrive/Google Drive/UBI/Projects/froggy/examples/cookbook/docs/main.js",
    "group": "/home/tiagomiguelcs/SynologyDrive/Google Drive/UBI/Projects/froggy/examples/cookbook/docs/main.js",
    "groupTitle": "/home/tiagomiguelcs/SynologyDrive/Google Drive/UBI/Projects/froggy/examples/cookbook/docs/main.js",
    "name": ""
  },
  {
    "type": "post",
    "url": "/cookbook/auth/login",
    "title": "Login Example",
    "name": "authenticate",
    "description": "<p>Example of an Authentication Service using sqlite3 and the froggy framework.</p>",
    "group": "Guest",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "defaultValue": "kermit@muppets.com",
            "description": "<p>Email of the user.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "psw",
            "defaultValue": "123",
            "description": "<p>User's password.</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Example usage:",
        "content": "curl -d \"email=kermit@muppets.com&psw=123\" -X POST http://localhost:5000/cookbook/auth/login",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "/home/tiagomiguelcs/SynologyDrive/Google Drive/UBI/Projects/froggy/examples/cookbook/cookbook/__init__.py",
    "groupTitle": "Guest",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/auth/login"
      }
    ]
  },
  {
    "type": "get",
    "url": "/cookbook/hello_world/:name",
    "title": "Hello World Example",
    "name": "demo",
    "group": "Guest",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of the guest.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "message",
            "description": "<p>The Hello World Message.</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Example usage:",
        "content": "curl -i http://localhost:5000/cookbook/hello_world/Anna",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "/home/tiagomiguelcs/SynologyDrive/Google Drive/UBI/Projects/froggy/examples/cookbook/cookbook/__init__.py",
    "groupTitle": "Guest",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/hello_world/:name"
      }
    ]
  },
  {
    "type": "get",
    "url": "/cookbook/auth/logout",
    "title": "Logout Example",
    "name": "logout",
    "description": "<p>Server side logout using the JWT token.</p>",
    "group": "User",
    "examples": [
      {
        "title": "Example usage:",
        "content": "curl -H \"Authorization: <token>\" http://localhost:5000/cookbook/auth/logout",
        "type": "curl"
      }
    ],
    "header": {
      "fields": {
        "Authorization": [
          {
            "group": "Authorization",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Web Token</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "/home/tiagomiguelcs/SynologyDrive/Google Drive/UBI/Projects/froggy/examples/cookbook/cookbook/__init__.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/auth/logout"
      }
    ]
  },
  {
    "type": "get",
    "url": "/cookbook/auth/secure",
    "title": "Secured Service Example",
    "name": "secure",
    "description": "<p>Autorization Service, the secure service can only be accessed if the user has a valid authorization issued by froggy.</p>",
    "group": "User",
    "examples": [
      {
        "title": "Example usage:",
        "content": "curl -H \"Authorization: <token>\" http://localhost:5000/cookbook/auth/secure",
        "type": "curl"
      }
    ],
    "header": {
      "fields": {
        "Authorization": [
          {
            "group": "Authorization",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Web Token</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "/home/tiagomiguelcs/SynologyDrive/Google Drive/UBI/Projects/froggy/examples/cookbook/cookbook/__init__.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/auth/secure"
      }
    ]
  }
] });
