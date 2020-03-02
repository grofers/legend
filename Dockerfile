FROM python:3.7

ENV LEGEND_HOME = /src
ENV GRAFONNET_REPO_URL = "https://github.com/grofers/grafonnet-lib"
ENV GRAFONNET_REPO_NAME = "grafonnet-lib"

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kubernetes/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . /src

RUN pip install .

RUN mkdir /src/.legend

CMD kopf run /src/kubernetes/handler.py
