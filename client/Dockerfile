# Start from the official latest Python base image
FROM python:3.11

# Set the current working directory to /client
WORKDIR /client

COPY requirements.txt /client/requirements.txt

RUN pip install -r /client/requirements.txt

COPY . .

EXPOSE 5555

# run the client
CMD ["python", "./main.py", "-it"]

