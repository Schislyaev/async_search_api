FROM python:3.10.7

WORKDIR /opt/app

COPY functional/requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY functional functional/

COPY entrypoint_tests.sh /
COPY pytest.ini pytest.ini

WORKDIR /opt/app/functional

ENTRYPOINT ["sh", "/entrypoint_tests.sh"]
