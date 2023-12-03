FROM python:3.11.4-alpine

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

RUN apk update;
RUN apk add unzip;
RUN apk add openjdk11-jre-headless;

RUN mkdir /jars

RUN cd /jars; wget https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip; \

RUN cd /jars; if [ -e stanford-corenlp-4.2.2.zip ]; then unzip stanford-corenlp-4.2.2.zip; fi

CMD [ "python", "main.py" ]
