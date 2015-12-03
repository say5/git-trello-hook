# Pull base image.
FROM python:2.7
MAINTAINER Alexander Svyrydov

ADD . /git2trello

WORKDIR /git2trello

RUN rm -f .env && pip install -r requirements.txt

EXPOSE 7575

ENV PORT 7575

CMD ./git2trello.py
