FROM python:3.9.5
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get install -y unzip && \
    apt-get clean;

COPY . .

RUN rm /Dockerfile; rm /Jenkinsfile;

RUN cd /jars; wget http://nlp.stanford.edu/software/stanford-corenlp-latest.zip; exit 0; 
RUN if [ -e stanford-corenlp-latest.zip ]; then cd /jars; rm -Rf stanford-corenlp-4.2.2; unzip stanford-corenlp-latest.zip; rm stanford-corenlp-latest.zip; fi

CMD [ "python", "main.py" ]
