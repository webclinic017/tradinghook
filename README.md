# INTRODUCTION

TODAYS PURPOSE IS JUST TO PLACE THIS FILE TO ACT AS A PLACEHOLDER.

"tradinghook" is a FLask based application that is designed to "catch" hooks and then place trades based on the alert.
I am balancing what I have in GITHUB with what I have in production.  My Production version isn't perfect yet... in fact it is scary because I have used it to place trades.   

It is designed to be able to place trade on Webull.  Both paper and live.  It is in the process of being setup to trade with Alpaca as well as TD Ameritrade.

It is being designed to use a Condition chain that allows the operator to decide if which exchanges they want to place a trade [buy or sell] on.  This would include having a single alert place trades in multiple exchanges at once using different stratgies.
The strategies being designed might be to MAX out everything.  Or - by design - to creaet a sub-pool reserved from the account and to balance trading so as to be able to place a trade in each of the trading days.

In the process I will incorporate a number of features.  1) Monitor reality and make sure a "sell" transaction is acted on.  It is possible in a fast moving enviornment for a trade being placed to already be out of the action and would otherwise just sit.  2) Sync accounts to verify settled and unsettled acounts as well as ingest changes caused by dividends.

You can use it for

- trading.
- fun

## INSTALLATION

```bash
git clone https://github.com/tlh45342/tradinghook.git
```

To make sure you have all the python modules installed.

```bash
pip install -r requirements.txt

## STRUCTURE

    ├── CHANGES                     Change logs
    ├── README.markdown
    ├── fabfile.py                  Fabric file to automated managament project
    ├── fbone.conf                  Apache config
    ├── requirements.txt            3rd libraries
    ├── tests.py                    Unittests
    ├── wsgi.py                     Wsgi app
    ├── fbone
       ├── __init__.py
       ├── app.py                   Main App
       ├── config.py                Develop / Testing configs
       ├── constants.py             Constants
       
## LICENSE

tradinghook is licensed under the Apache License, Version 2.0. See LICENSE for the full license text.

## ACKNOWLEDGEMENTS

Many thanks to Python, Flask and other good stacks.       
