#!/bin/sh

. ./.env

./git-trello-hook.py -k $API_KEY -t $OAUTH_TOKEN
