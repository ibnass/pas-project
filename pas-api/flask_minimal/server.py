from typing_extensions import Required
from flask import Flask, request
from flask.ext.restful import Resource, Api, marshal_with, fields, abort
from flask_restful_swagger import swagger
from flask_restful import reqparse
from flask_minimal.api import AmazonEndpoint,IbmEndpoint, DummyEndpoint, HelloEndpoint,GoogleEndpoint
from flask_cors import CORS

API_VERSION_NUMBER = '1.0'
API_VERSION_LABEL = 'v1'



class CustomFlaskApp(object):

    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        custom_errors = {
            'JsonInvalidError': {
                'status': 500,
                'message': 'JSON format not valid'
            },
            'JsonRequiredError': {
                'status': 400,
                'message': 'JSON input required'
            }
        }
        self.api = swagger.docs(Api(self.app, errors=custom_errors), apiVersion=API_VERSION_NUMBER)
        
        self.api.add_resource(DummyEndpoint, '/dummy', endpoint='dummy')
        self.api.add_resource(AmazonEndpoint,'/amazon', endpoint = 'amazon')
        self.api.add_resource(IbmEndpoint, '/ibm', endpoint='ibm')
        self.api.add_resource(HelloEndpoint, '/hello', endpoint='hello')
        self.api.add_resource(GoogleEndpoint, '/google', endpoint='google')


    def run(self, *args, **kwargs):
        self.app.config['PROPAGATE_EXCEPTIONS'] = False
        self.app.run(*args, **kwargs)


def run_app(*args, **kwargs):
    app = CustomFlaskApp()
    app.run(*args, **kwargs)


if __name__ == '__main__':
    run_app(debug=True)
