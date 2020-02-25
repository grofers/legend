FROM python:3.7
WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY kubernetes/requirements.txt .
RUN pip install -r requirements.txt

ADD . /src

RUN pip install .
RUN rm -rf *

CMD kopf run handler.py
