FROM python:3.6

WORKDIR /var/www/metadash

COPY Pipfile ./

RUN pip install pipenv --no-cache-dir

RUN pipenv --three install
