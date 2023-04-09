FROM python:3.10.7

WORKDIR /opt/app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY postgres_to_es postgres_to_es/

WORKDIR /opt/app/postgres_to_es

CMD ["python", "etl_service.py"]
