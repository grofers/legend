FROM bitnami/jsonnet AS jsonnet
RUN echo "`which jsonnet`"

FROM python:3.7

ENV LEGEND_HOME = /src
ENV GRAFONNET_REPO_URL = "https://github.com/grofers/grafonnet-lib"
ENV GRAFONNET_REPO_NAME = "grafonnet-lib"

WORKDIR /src

COPY --from=jsonnet /opt/bitnami/jsonnet/bin/jsonnet /usr/local/bin/jsonnet

COPY requirements.txt .

RUN sed -i '/jsonnet/d' requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY kubernetes/requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

ADD . /src

RUN sed -i '/jsonnet/d' requirements.txt

RUN pip install .

RUN mkdir /src/.legend

CMD kopf run /src/kubernetes/handler.py
