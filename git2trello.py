#!/usr/bin/env python

import argparse
from gevent import monkey;monkey.patch_all()
from bottle import route, request,run, default_app
from trello import Cards, Lists
import re
import json
import os

def get_args():
    defaults = {
        'listen-iface': '0.0.0.0',
        'listen-port': 7575,
    }

    description = 'Trello Git integration'
    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=formatter_class)
    parser.add_argument('-k', '--api-key',
                        type=str,
                        help='Trello API Key',
                        default=os.environ.get('API_KEY'),
                        dest='api_key')
    parser.add_argument('-t', '--oauth-token',
                        type=str,
                        help='Trello Oauth token (see readme.md for more info)',
                        default=os.environ.get('OAUTH_TOKEN'),
                        dest='oauth_token')
    parser.add_argument('-l', '--listen-on',
                        type=str,
                        help='Interface to listen on',
                        default=os.environ.get("IFACE", defaults['listen-iface']),
                        dest='listen_iface')
    parser.add_argument('-p', '--port',
                        type=int,
                        help='Bind to port',
                        default=int(os.environ.get("PORT", defaults['listen-port'])),
                        dest='listen_port')
    return parser.parse_args()


@route("/")
def index():
    return 'git webhook to comment on Trello cards'


@route("/webhook", method='POST')
def handle_payload():
    json_payload = None
    from_gitlab = False
    if request.get_header('Content-Type', None) == 'application/json':
        json_payload = request.json
        from_gitlab = True
    else:
        body = request.forms['payload']
        json_payload = json.loads(body)
    print(json_payload)
    if 'commits' not in json_payload['commits']:
        return "done"
    commits = json_payload['commits']
    cards_in_commit = []
    cards_url_dict = {}
    card_pattern = '\[([a-z0-9]{8})\]'

    for commit in commits:
        cards_in_commit[:] = []
        results = re.findall(
            card_pattern, commit['message'], flags=re.IGNORECASE)
        for result in results:
            cards_in_commit.append(result)
        if cards_in_commit:
            for card in cards_in_commit:
                comment = '{0}\n{1}'.format(
                    commit['message'].replace('['+card+']', ''), commit['url'])
                TRELLO_CARDS.new_action_comment(card, comment)

    return "done"


def main():
    args = get_args()
    global TRELLO_CARDS
    TRELLO_CARDS = Cards(args.api_key, args.oauth_token)
    run(host=args.listen_iface, port=args.listen_port, server='gevent', debug=True)


if __name__ == '__main__':
    main()


app = default_app()
