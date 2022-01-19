from typing import Text, final
from flask import request
from flask_restful import reqparse
from numpy.core.numeric import False_
from flask.ext.restful import Resource, Api, marshal_with, fields, abort
from flask_restful_swagger import swagger
from .models import DummyResult,SpeechResult,MetricResult
from .models import HelloResult
from .errors import JsonRequiredError
from .errors import JsonInvalidError
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import boto3
import time
import numpy as np
import urllib
import json
from datetime import datetime

# TRANSCRIBE_CLIENT = boto3.client('transcribe')

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help="Video number")
parser.add_argument('ref', type=str, help="Reference text")
parser.add_argument('hypo', type=str, help="Hypothis text")


class BaseSpeech(Resource):

    def get_video_id(self, id):

        video_dict = {1 : 'video_1.mp3',
        2 : "video_2.mp3",
        3: "video_3.mp3",
        4 :"video_4.mp3"
        }

        return video_dict.get(id)

class GoogleEndpoint(BaseSpeech):
    @swagger.operation(
        responseClass=SpeechResult.__name__,
        nickname='google'
    )

    def get_transcribe(self,id_):
        import json

        with open("./audios/transcripts.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()

        transcript = jsonObject[id_]
        return SpeechResult(transcript)

    @marshal_with(SpeechResult.ressource_fields)
    def get(self):
        
        video_id = parser.parse_args().get('id')

        return self.get_transcribe(str(video_id))

class IbmEndpoint(BaseSpeech):
    @swagger.operation(
        responseClass=SpeechResult.__name__,
        nickname='ibm'
    )

    def get_transcribe(self,path):

       apikey='YktrQT3qjabSy_c08NtElsfY8R8sg1VCP_ATEfncf4j5'
       region ='eu-gb'
       url='https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/36f6a32f-1dbb-4ce1-93f3-f24816bf103a'

       authenticator = IAMAuthenticator(apikey)
       stt=SpeechToTextV1(authenticator=authenticator)
       stt.set_service_url(url)

       with open(path,'rb') as file:
           res = stt.recognize(audio=file, content_type='audio/mp3', model='en-US_BroadbandModel').get_result()
        
       txt = ""
       for i in range(len(res['results'])):
          txt += " "+res['results'][i]['alternatives'][0]['transcript']
       return SpeechResult(txt)

    @marshal_with(SpeechResult.ressource_fields)
    def get(self):
        
        video_id = parser.parse_args().get('id')
        video_path = self.get_video_id(video_id)
        path = './audios/' + video_path

        return self.get_transcribe(path)


class AmazonEndpoint(BaseSpeech):

    @swagger.operation(
        responseClass=SpeechResult.__name__,
        nickname='amazon'
    )

    @marshal_with(SpeechResult.ressource_fields)
    def get(self):

        transcribe_client = boto3.client('transcribe')

        job_name = datetime.now().strftime("%m%d%Y%H%M%S") + "__job"

        video_id = parser.parse_args().get('id')
        video_path = self.get_video_id(video_id)
        
        file_uri = 's3://pas-audio/' + video_path

        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat='mp3',
            LanguageCode='en-US'
        )

        max_tries = 60
        while max_tries > 0:
            max_tries -= 1
            job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                print(f"Job {job_name} is {job_status}.")
                if job_status == 'COMPLETED':
                    response = urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                    data = json.loads(response.read())
                    res = data['results']['transcripts'][0]['transcript']
                    return SpeechResult(res)
                break
            else:
                print(f"Waiting for {job_name}. Current status is {job_status}.")
            time.sleep(10)

        return final




class DummyEndpoint(Resource):
    @swagger.operation(
        responseClass=DummyResult.__name__,
        nickname='dummy')
    
    
    
    @marshal_with(DummyResult.resource_fields)
    def get(self):
        """Return a DummyResult object

        Lightweight response to let us confirm that the server is on-line"""
        return DummyResult()


class HelloEndpoint(Resource):
    @swagger.operation(
        responseClass=HelloResult.__name__,
        nickname='hello',
        responseMessages=[
            {"code": 400, "message": "Input required"},
            {"code": 500, "message": "JSON format not valid"},
        ],
        parameters=[
            {
                "name": "name",
                "description": "JSON-encoded name",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            },
        ])
    @marshal_with(HelloResult.resource_fields)
    def post(self):
        """Return a HelloResult object"""
        reqs = request.get_json()
        if not reqs:
            raise JsonRequiredError()
        try:
            reqs['name']
            return HelloResult(name=reqs['name'])
        except KeyError:
            raise JsonInvalidError()
