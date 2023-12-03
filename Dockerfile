FROM python:3.11.4-alpine

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

RUN apk update;
RUN apk add unzip;
RUN apk add openjdk11-jre-headless;

RUN mkdir /jars

RUN cd /jars; wget https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip; \
    if [["$?" -ne "0"]]; \
    then rm stanford-corenlp-latest.zip; \
    else rm /jars/stanford-corenlp-4.2.2/; \
    fi; exit 0; 

RUN cd /jars; if [ -e stanford-corenlp-latest.zip ]; then unzip stanford-corenlp-latest.zip; rm stanford-corenlp-latest.zip; fi

CMD [ "python", "main.py" ]
