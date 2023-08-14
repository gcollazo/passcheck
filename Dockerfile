FROM python:3.11-slim

RUN apt update && apt install -y make
RUN useradd -m apprunner

USER apprunner

WORKDIR /usr/src/app
RUN pip install --upgrade pip pip-tools
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 1337

CMD "python -m flask --app app run --host 0.0.0.0 --port 1337"
