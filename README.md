# ChatExercise
Chat Server

## 1. using docker-compose builds, (re)creates, starts all the containers:
docker-compose build
docker-compose up -d

## 2. build the client docker image and run the 2 or more docker containers:
docker build -t client_image .
docker run --network=host -p 5555:5555 -it --name client_container1 client_image
docker run --network=host -p 5555:5555 -it --name client_container2 client_image    

## stop docke container & rm all images:
docker-compose down
docker image prune -a -f
docker stop <container_name>
docker rmi <image_id>

## open swagger getting API documentation:
open URL: http://127.0.0.1:8000/docs

# working locally without docker (Windows  machine):

## only 1st time create virtual env:
py -m venv env

## activaite virtual env from vscode terminal:
Set-ExecutionPolicy Unrestricted -Scope Process
.\env\Scripts\activate

## install requirements:
py -m pip install -r requirements.txt

## running server (or from vscode run Python: FastAPI server from launch.json):
py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

## running client (or from vscode run client from launch.json):
py ./main.py

