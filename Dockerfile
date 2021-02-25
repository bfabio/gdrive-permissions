FROM python:3.8-slim

RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
WORKDIR /app

COPY . /app

CMD ["python", "gdrive.py"]
