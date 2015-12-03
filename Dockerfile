# Pull base image.
FROM python:2.7
MAINTAINER Alexander Svyrydov

ADD . /git-trello-hook

WORKDIR /git-trello-hook

RUN pip install -r requirements.txt

CMD ./start.sh
