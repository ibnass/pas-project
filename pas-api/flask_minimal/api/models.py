from flask.ext.restful import Resource, Api, marshal_with, fields, abort
from flask_restful_swagger import swagger

@swagger.model
class DummyResult(object):
    """The result of a call to /dummy"""
    resource_fields = {
        'dummy': fields.String
    }

    def __init__(self):
        self.dummy = "foobar"

@swagger.model
class SpeechResult(object):
    ressource_fields = {
        'result' : fields.String
    }

    def __init__(self,res=None):
        self.result = res

@swagger.model
class MetricResult(object):
    ressource_fields = {
        'result' : fields.Float
    }

    def __init__(self,res=None):
        self.result = res


@swagger.model
class HelloResult(object):
    """The result of a call to /hello"""
    resource_fields = {
        'greetings': fields.String
    }

    def __init__(self, name):
        self.greetings = "Hello {}".format(name)
