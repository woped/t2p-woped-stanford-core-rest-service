FROM python:3.9.5
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;
COPY . .
CMD [ "python", "main.py" ]
