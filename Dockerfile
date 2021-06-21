FROM python:3.9.5
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get install -y unzip && \
    apt-get clean;

RUN mkdir /jars
RUN cd /jars; wget http://nlp.stanford.edu/software/stanford-corenlp-latest.zip
RUN cd /jars; unzip stanford-corenlp-latest.zip
COPY . .
CMD [ "python", "main.py" ]
