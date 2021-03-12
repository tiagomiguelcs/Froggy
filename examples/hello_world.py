"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-

Froggy Hello World Demo Service.
"""
from froggy import framework
from flask import Flask, request
from handlers.hops import frogify
from handlers.gadgets import print, json_response

@frogify('/examples/hello_world/<name>', authorization=False, methods=['GET'])
def demo(name):
    """
    @api {get} /examples/hello_world/:name Hello World Demo Service 
    @apiName demo 
    @apiGroup Guest
    @apiParam {String} name Name of the guest.
    @apiSuccess {String} message The Hello World Message. 
    @apiExample {curl} Example usage:
        curl -i http://localhost:5000/examples/hello_world/Anna
    """
    #@apiHeader (Authorization) {String} JWT Web Token
    data={"message": "Hello World, "+name}
    return json_response(data)
