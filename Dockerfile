FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y curl
RUN mkdir /src
COPY requirements.txt /src
WORKDIR /src
RUN pip install -r /src/requirements.txt

COPY crypto.py /src
COPY search.py /src
COPY run.sh /src

CMD ./run.sh
