FROM bitnami/jsonnet AS jsonnet
RUN echo "`which jsonnet`"

FROM python:3.7

ENV LEGEND_HOME="/src"
ENV GRAFONNET_REPO_URL="https://github.com/grafana/grafonnet-lib"
ENV GRAFONNET_REPO_NAME="grafonnet-lib"
ENV GRAFONNET_REPO_RELEASE_TAG="v0.1.0"

WORKDIR /src

COPY --from=jsonnet /opt/bitnami/jsonnet/bin/jsonnet /usr/local/bin/jsonnet

COPY requirements.txt .

RUN sed -i '/jsonnet/d' requirements.txt

RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

COPY kubernetes/requirements.txt .

RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

ADD . /src

RUN sed -i '/jsonnet/d' requirements.txt

RUN pip install .

# Installing jq for testing 
RUN apt-get update && apt-get install -y \
    jq && rm -rf /var/lib/apt/lists/*

RUN chmod u+x /src/run_tests.sh

CMD kopf run /src/kubernetes/handler.py
