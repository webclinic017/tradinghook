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

## COMPONENTS

### Frontend

- [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate)
- [jQuery](http://jquery.com/)
- [Twitter Bootstrap](https://github.com/twitter/bootstrap)
- [Jinja2](http://jinja.pocoo.org/docs/dev/)

### Flask Extensions

- [SQLAlchemy](http://www.sqlalchemy.org) and [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org)
- [WTForms](http://wtforms.readthedocs.io) and [Flask-WTF](https://flask-wtf.readthedocs.io).
- [Flask-Login](https://flask-login.readthedocs.io)
- [Flask-Testing](https://pythonhosted.org/Flask-Testing/)
- [Flask-RESTful](http://flask-restful-cn.readthedocs.io/)

### Others

- Modular Applications with Blueprints.
- Use [Sentry](https://getsentry.com) for real-time crash reporting.
- Automated managament via [fabric](http://flask.pocoo.org/docs/patterns/fabric/)

## USAGE

Pre-required Setup:

- MacOS/Ubuntu (should be fine in other linux distro)
- git
- Python / pip / Fabric
- sqlite / MySQL
- Apache + mod\_wsgi

    git clone https://github.com/imwilsonxu/fbone.git fbone

    fab setup_python_macos
    fab bootstrap
    fab test
    fab debug

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
       
## TODO

- Upgrade to [Python3k](https://www.python.org/download/releases/3.0/).
- User [Celery](http://celeryprojet.org), distributed task queue.

## LICENSE

Apache

## ACKNOWLEDGEMENTS

Many thanks to Python, Flask and other good stacks.       
