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
