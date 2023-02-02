# ChatExercise
Chat Server

## build a docker image and run the docker container:
docker build -t chatImage .
docker run -d --name chatContainer -p 8000:8000 chatImage

## or just using docker-compose builds, (re)creates, starts all the containers:
docker-compose build
docker-compose up -d
docker-compose down

## open bash from docker:

## open swagger getting API documentation:
open URL: http://127.0.0.1:8000/docs

# working locally without docker (Windows  machine):

## only 1st time create virtual env:
py -m venv env

## activaite virtual env:
Set-ExecutionPolicy Unrestricted -Scope Process
.\env\Scripts\activate

## install requirements:
py -m pip install -r requirements.txt

## running server:
py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

## running client:
py ./main.py

