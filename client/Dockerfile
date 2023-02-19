# Start from the official latest Python base image
FROM python:3.11

# Set the current working directory to /client
WORKDIR /client

COPY requirements.txt /client/requirements.txt

RUN pip install -r /client/requirements.txt

# copies all client app files in host machine current directory to  /client directory in the container.
COPY . .

EXPOSE 5555

# run the client
CMD ["python", "./main.py", "-it"]

