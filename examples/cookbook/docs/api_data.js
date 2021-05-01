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
    "title": "User Login",
    "name": "authenticate",
    "description": "<p>Example of an authentication service using sqlite3 and the froggy framework.</p>",
    "group": "Authentication",
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
    "groupTitle": "Authentication",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/auth/login"
      }
    ]
  },
  {
    "type": "get",
    "url": "/cookbook/auth/logout",
    "title": "User Logout",
    "name": "logout",
    "description": "<p>Example of a server side logout service that uses previously issued JWT tokens to logout an authenticated user.</p>",
    "group": "Authentication",
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
    "groupTitle": "Authentication",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/auth/logout"
      }
    ]
  },
  {
    "type": "get",
    "url": "/cookbook/auth/secure",
    "title": "Secure Service",
    "name": "secure",
    "description": "<p>Example of a secure service that can only be accessed if the user has a valid authorization token issued by froggy.</p>",
    "group": "Authentication",
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
    "groupTitle": "Authentication",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/auth/secure"
      }
    ]
  },
  {
    "type": "get",
    "url": "/cookbook/databases/sqlite3/:statement",
    "title": "Data Manipulation",
    "description": "<p>Example of a service that implements and executes several SQL statements for data manipulation using froggy's database API.</p>",
    "name": "database",
    "group": "Databases",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "statement",
            "description": "<p>Select a sql statement (SELECT, INSERT, UPDATE, or DELETE)</p>"
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
            "field": "Returns",
            "description": "<p>the result of the selected SQL statement.</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Example usage:",
        "content": "curl -i http://localhost:5000/cookbook/databases/sqlite3/SELECT",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "/home/tiagomiguelcs/SynologyDrive/Google Drive/UBI/Projects/froggy/examples/cookbook/cookbook/__init__.py",
    "groupTitle": "Databases",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/databases/sqlite3/:statement"
      }
    ]
  },
  {
    "type": "get",
    "url": "/cookbook/hello_world/:name",
    "title": "Hello World",
    "name": "demo",
    "description": "<p>Example of a simple 'Hello World' service.</p>",
    "group": "Generic",
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
    "groupTitle": "Generic",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/cookbook/hello_world/:name"
      }
    ]
  }
] });
