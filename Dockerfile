FROM bitnami/jsonnet AS jsonnet
RUN echo "`which jsonnet`"

FROM python:3.9.5

ENV LEGEND_HOME="/src"
ENV GRAFONNET_REPO_URL="https://github.com/grafana/grafonnet-lib"
ENV GRAFONNET_REPO_NAME="grafonnet-lib"
# Update to latest commit on master at this point in time since no new releases are being cut. This is better 
# than using master tag since new backward incompatible commits into master might break legend altogether.
ENV GRAFONNET_REPO_RELEASE_TAG="3082bfca110166cd69533fa3c0875fdb1b68c329"

WORKDIR /src

COPY --from=jsonnet /opt/bitnami/jsonnet/bin/jsonnet /usr/local/bin/jsonnet

COPY requirements.txt .

RUN sed -i '/jsonnet/d' requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY kubernetes/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD . /src

RUN sed -i '/jsonnet/d' requirements.txt

RUN pip install .

# Installing jq for testing 
RUN apt-get update && apt-get install -y \
    jq && rm -rf /var/lib/apt/lists/*

RUN chmod u+x /src/run_tests.sh

CMD kopf run /src/kubernetes/handler.py
