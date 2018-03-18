FROM python:2.7
RUN apt-get update
RUN apt-get install -y vim-nox build-essential
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /opt/project
