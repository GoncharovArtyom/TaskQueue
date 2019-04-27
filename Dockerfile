FROM python:3.7.3-stretch

ADD . /TaskQueue
WORKDIR /TaskQueue

RUN chmod +x ./wait-for-it.sh
RUN pip3 install -r requirements.txt

