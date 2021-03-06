# INTRODUCTION

"tradinghook" is a Flask based application that is designed to "catch" hooks and then place trades based on the alert.
I am balancing what I have in GITHUB with what I have in production.  My Production version isn't perfect yet... in fact it is scary because I have used it to place trades.   

It is designed to be able to place trade on Webull.  Both paper and live.  It is in the process of being setup to trade with Alpaca as well as TD Ameritrade.

It is being designed to use a Condition chain that allows the operator to decide if which exchanges they want to place a trade [buy or sell] on.  This would include having a single alert place trades in multiple exchanges at once using different stratgies.
The strategies being designed might be to MAX out everything.  Or - by design - to creaet a sub-pool reserved from the account and to balance trading so as to be able to place a trade in each of the trading days.

In the process I will incorporate a number of features.  1) Monitor reality and make sure a "sell" transaction is acted on.  It is possible in a fast moving enviornment for a trade being placed to already be out of the action and would otherwise just sit.  2) Sync accounts to verify settled and unsettled acounts as well as ingest changes caused by dividends.

## Status

Posted 10/17/2021 - Yes this is an active project.  There will be updates to this on a regular basis.  No I do not see this as being a trivial project .. but I want it done.

## Docs

Please read the "theory-of-operation.rst" file.  Or at least this is what I am posting at the moment.  This will be more of a introduction of how this can be used.
This also reveals some of the current internal workings of how the "structures" json file can be used to implement a set of primitive trading conditions.

## INSTALLATION

```bash
git clone https://github.com/tlh45342/tradinghook.git
```

To make sure you have all the python modules installed.

```bash
pip install -r requirements.txt
```

## SIDEBAR: Notes for creating a service for Linux based distributions

I am putting my notes here now - because I will use them.  Consider these random notes used to implement the Flask APP as a service.

To create a service entry cd /etc/systemd/system
Create a file that looks something like is found in the following block.
I am naming mine: tradinghook.service
As much as I hate assumptions - you will need to edit this to your tastes and for your environment.

```bash
cat <<EOF | sudo tee /etc/systemd/system/tradinghook.service
[Unit]
Description=tradinghook.service

[Service]
WorkingDirectory=/opt/tradinghook/
ExecStart=/usr/local/bin/gunicorn --certfile=cert.pem --keyfile=privkey.pem -b 0.0.0.0:443 -w 4 server:app

[Install]
WantedBy=multi-user.target
EOF
```

The key commands for reference are: 

```bash
sudo systemctl daemon-reload
sudo systemctl start tradinghook
sudo systemctl restart tradinghook
sudo systemctl stop tradinghook
sudo systemctl status tradinghook
```

## STRUCTURE

    ????????? CHANGES.md                      Change logs
    ????????? requirements.txt                3rd libraries
    ????????? config.py                       global inheritance of application values
    ????????? server.py                       Server code
    ????????? app
       ????????? doc
       |   ????????? theory-of-operation.md   Theory behind the intended use
       |   ????????? structures.md            structures - reference      
       ????????? static
       ????????? templates
       ????????? __init__.py
       ????????? routes.py                    basic route statements
       ????????? tradecode.py                 routines for trading and management
       ????????? user_db.py                   User DB management
       ????????? common_db.py                 Commond db routines
       
## LICENSE

tradinghook is licensed under the Apache License, Version 2.0. See LICENSE for the full license text.

## ACKNOWLEDGEMENTS

Many thanks to Python, Flask and other good stacks.       
