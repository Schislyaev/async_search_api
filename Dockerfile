FROM python:3.10.7-alpine

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src/

COPY entrypoint.sh /

WORKDIR /opt/app/src

ENTRYPOINT ["sh", "/entrypoint.sh"]
