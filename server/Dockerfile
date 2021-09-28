FROM python:3.8-alpine

COPY ./shnootalk_cc_server ./shnootalk_cc_server
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system

CMD gunicorn -w 1 -b 0.0.0.0:8000 shnootalk_cc_server:app
