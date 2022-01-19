# Pas Project

This application has been created in aim to compare different speech-to-text APIs.

To start using this web application localy, we have to lunch the flask api (back-end) then the angular application (front-end).

First lunch the back-end:

```
cd pas-api
source venv/Scripts/activate
pip install -r requirements.txt
python runserver.py
```
or
`source launch-api.txt`


Then the front-end (launch-app.txt):

```
cd pas-app
ng serve -o
```
or
`source launch-app.txt`

# Warning

To use the application, you have to setup AWS Credentials on your local environement. Explanations are available here : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
