FROM ubuntu:16.04
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]