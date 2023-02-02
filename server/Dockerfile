# Start from the official latest Python base image
FROM python:3.11

# Set the current working directory to /server
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . .

# run the uvicorn app server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]