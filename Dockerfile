FROM python:3.7-alpine
COPY . /app
WORKDIR /app

CMD ["python", "main.py"]
