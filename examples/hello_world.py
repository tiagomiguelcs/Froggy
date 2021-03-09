"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-

Froggy Hello World Demo Service.
"""
from flask import Flask, request
from handlers.hops import frogify
from handlers.gadgets import print, json_response


@frogify('/examples/hello_world', methods=['GET'])
def demo():
    data={"message": "Hello World"}
    return json_response(data)
