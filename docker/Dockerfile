FROM python:3.6
RUN apt-get update
RUN apt-get install -y vim-nox build-essential python-pygame
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH=/opt/project
RUN apt-get install telnet
WORKDIR /opt/project/cthulhuwars
