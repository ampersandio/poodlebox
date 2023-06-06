FROM python:3.10.0
WORKDIR /poodlebox-api
COPY . .
RUN apt-get update && apt-get install -y gcc wget
RUN wget https://dlm.mariadb.com/2319727/Connectors/c/connector-c-3.3.1/mariadb-connector-c-3.3.1-debian-9-stretch-amd64.tar.gz -O - | tar -zxf - --strip-components=1 -C /usr
RUN pip install -r ./requirements.txt
WORKDIR /poodlebox-api/app
CMD uvicorn main:app --host 0.0.0.0 --port 8000
