define({ "api": [
  {
    "type": "get",
    "url": "/examples/hello_world/:name",
    "title": "Hello World Demo Service",
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
        "content": "curl -i http://localhost:5000/examples/hello_world/Anna",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "examples/hello_world.py",
    "groupTitle": "Guest",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/examples/hello_world/:name"
      }
    ]
  },
  {
    "type": "post",
    "url": "/examples/auth/login",
    "title": "Authentication Service",
    "name": "demo",
    "description": "<p>Example of an Authentication Service using sqlite3 and the froggy framework.</p>",
    "group": "User",
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
        "content": "curl -d \"email=kermit@muppets.com&psw=123\" -X POST http://localhost:5000/examples/auth/login",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "examples/auth.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/examples/auth/login"
      }
    ]
  },
  {
    "type": "get",
    "url": "/examples/auth/logout",
    "title": "Logout Service",
    "name": "logout",
    "description": "<p>Server side logout using the JWT token.</p>",
    "group": "User",
    "examples": [
      {
        "title": "Example usage:",
        "content": "curl -H \"Authorization: <token>\" http://localhost:5000/examples/auth/logout",
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
    "filename": "examples/auth.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/examples/auth/logout"
      }
    ]
  },
  {
    "type": "get",
    "url": "/examples/auth/secure",
    "title": "Secured Service",
    "name": "secure",
    "description": "<p>Autorization Service, the secure service can only be accessed if the user has a valid authorization token issued by froggy.</p>",
    "group": "User",
    "examples": [
      {
        "title": "Example usage:",
        "content": "curl -H \"Authorization: <token>\" http://localhost:5000/examples/auth/secure",
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
    "filename": "examples/auth.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "http://localhost:5000/examples/auth/secure"
      }
    ]
  }
] });
