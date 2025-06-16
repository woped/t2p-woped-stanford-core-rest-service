FROM python:3.11.4-alpine

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

RUN apk update && \
    apk add unzip openjdk11-jre-headless wget

RUN mkdir -p /jars && \
    cd /jars && \
    wget --no-check-certificate https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip && \
    unzip stanford-corenlp-4.2.2.zip && \
    rm stanford-corenlp-4.2.2.zip

CMD [ "python", "main.py" ]
