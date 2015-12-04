# git2trelo

A github/gitlab webhook script written in python and based on [git-trello-hook](https://github.com/hewigovens/git-trello-hook).

##Objective

In git's commit add [CARDID] string (where CARDID - your Trello's Card ID, 8 symbols), 
in corresponding Trello card a comment will be added with text message and url to git comment.

##Configuration

###Script
Just pust lines in file `.env`:

        API_KEY='TRELLO_API_KEY'
        OAUTH_TOKEN='TRELLO_OAUTH_TOKEN_FOR_BOARD'
        
And run ./start.sh

By default script will bind port 7575 on all interfaces, it can be changed - see help.

###Docker
Update `.env` file, then:

        docker build -t git2trello .
        docker run -d -P --env-file=.env git2trello

###Docker-compose
Update `.env` file, then:

        docker-compose up

###Heroku
Add configuration variables API_KEY and OAUTH_TOKEN

## Trello integration

###`API_KEY`
https://trello.com/1/appKey/generate

###`OAUTH_TOKEN`
This is not so well explained in Trello, but I understood that you need to authorize the app with API_KEY to access each board separatelly. To do that:

https://trello.com/1/authorize?response_type=token&name=[BOARD+NAME+AS+SHOWN+IN+URL]&scope=read,write&expiration=never&key=[YOUR+API_KEY+HERE]

where [YOUR+API_KEY+HERE] is the one you entered in the previous step, while [BOARD+NAME+AS...] is, well, what it says. If your board url is 

https://trello.com/b/XLvlTFVA/git-trello

then you should type in "git-trello".

## Git integration

Configure webhook with /webhook URL, for example if your app is runnning on IP 123.45.67.89: `http://123.45.67.89:7575/webhook`

#Credits

* [git-trello](https://github.com/zmilojko/git-trello)
* [git-trello-hook](https://github.com/hewigovens/git-trello-hook)
