import json
from colorama import init, Fore, Style
from termcolor import colored
import sqlite3
from sqlite3 import Error
import pandas
import configparser
from flask import Flask, request, render_template, redirect, url_for
import logging
import config as CONFIG
from webull import webull
from webull import paper_webull
import alpaca_trade_api as tradeapi
from datetime import date
from app import common_db

# ------------------------------

class Account:

    def __init__(self):
      self.userid = 0
      self.fundid = 0
      self.exchangeid = 0
      self.settled = 0
      self.unsettled = 0
      
class Transaction:

    def __init__(self):
      self.userid = 0
      self.symbol = 0
      self.side = 0
      self.qty = 0
      self.price = 0.0
      self.orderplaced = ""
      self.orderfilled = ""      

# ------------------------------

def xstr(s):
    return '' if s is None else str(s)

# ------------------------------

def query_transactions():
    today = date.today()
    d1 = str(today.strftime("%Y-%m-%d"))
    conn = create_connection(CONFIG.DATABASE)
    #print(type(today))
    sqlite_statement = ("SELECT * FROM transactions WHERE orderplaced like \""+d1+"%\";")
    #print(sqlite_statement)
    cursor = conn.execute(sqlite_statement)
    out = {}
    df1 = pandas.DataFrame(out, columns = ['userid', 'symbol', 'side', 'qty','price','amount','orderplaced','orderfilled'])  
    for row in cursor:
        userid = {"userid": xstr(row[0])}
        #print(userid)
        symbol = {"symbol": xstr(row[1])}
        side = {"side": xstr(row[2])}
        qty = {"qty": xstr(row[3])}
        price = {"price": xstr(row[4])}
        amount = {"amount": xstr(row[5])}
        orderplaced = {"orderplaced": xstr(row[6])}
        #print(orderplaced) 
        orderfilled = {"orderfilled": xstr(row[7])}
        #print("<",orderfilled,">")
        bar = {**userid, **symbol, **side, **qty, **price, **amount, **orderplaced, **orderfilled}
        df1 = df1.append(bar,ignore_index=True)
    return df1

# ------------------------------

def query_accountbalance(fundid):
    conn = create_connection(CONFIG.DATABASE)
    #print(fundid)
    #print(type(fundid))
    sqlite_statement = ("SELECT * FROM accountbalance WHERE fundid = \""+str(fundid)+"\";")
    #print(sqlite_statement)
    cursor = conn.execute(sqlite_statement)
    account = Account()
    for row in cursor:
      account.userid = int(row[0])
      account.fundid = int(row[1])
      account.exchangeid = int(row[2])
      account.settled = float(row[3])
      account.unsettled = float(row[4])
    #for row in cursor:
    #  print("userid = ", row[0])
    #  print("fundid = ", row[1])
    #  print("exchangeid = ", row[2])
    #  print("settled = ", row[3])
    #  print("unsettled = ", row[4], "\n") 
    return account

# ------------------------------

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# -------------------------------------------------------------------

def have_position(x):
    rows = []
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        query = ("SELECT * FROM position WHERE ticker = '"+x+"';")                             
        cursor = conn.cursor()
        count = cursor.execute(query)
        rows = cursor.fetchall() 
        #print ("OUT:",rows)
        cursor.close()
    else:
        print("Error! cannot create the database connection.")
    if rows == []:
        found = False
    else:
        found = True    
    return found

# -------------------------------------------------------------------

def return_position(x):
    rows = []
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        query = ("SELECT * FROM position WHERE 1=1;")                             
        cursor = conn.cursor()
        count = cursor.execute(query)
        rows = cursor.fetchall() 
        cursor.close()
    else:
        print("Error! cannot create the database connection.")
    return rows

# -------------------------------------------------------------------

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# ------------------------------------------------------------------- 
    
def create_accountbalance():
    sql_create_trades_table = """ CREATE TABLE IF NOT EXISTS accountbalance (
                                        userid text,
                                        fundid text,
                                        exchangeid text,
                                        settled text,
                                        unsettled text
                                    ); """
    # create a database connection
    conn = create_connection(CONFIG.DATABASE)
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_trades_table)
    else:
        print("Error! cannot create the database connection.")

# ------------------------------

def create_transactions_table():    
    sql_create_transactions_table = """ CREATE TABLE IF NOT EXISTS transactions (
                                        userid text,
                                        symbol text,
                                        side  text,   
                                        qty text,
                                        price  text,
                                        amount text,
                                        orderplaced text,
                                        orderfilled text
                                    ); """
    # create a database connection
    conn = create_connection(CONFIG.DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, sql_create_transactions_table)
    else:
        print("Error! cannot create the database connection.")
 
# ------------------------------

def create_position_table():    
    sql_create_table = """ CREATE TABLE IF NOT EXISTS position (
                           time text,
                           symbol text,
                           side  text,   
                           qty text,
                           price  text,
                           amount text
                        ); """
    # create a database connection
    conn = create_connection(CONFIG.DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, sql_create_transactions_table)
    else: 
        print("Error! cannot create the database connection.")
        
 
# ------------------------------

def insert_into_accountbalance(account):
    conn = create_connection(CONFIG.DATABASE)
    print(account)
    print(type(account))
    sqlite_statement = ("INSERT INTO accountbalance (userid,fundid,exchangeid,settled,unsettled)\n" +
                           "VALUES(\""+str(account['userid'])+"\"," +
                             "\""+str(account['fundid'])+"\","+
                             "\""+str(account['exchangeid'])+"\","+
                             "\""+str(account['settled'])+"\","+
                             "\""+str(account['unsettled'])+"\");")
    print(sqlite_statement)
    cursor = conn.cursor()
    count = cursor.execute(sqlite_statement)
    conn.commit()
    print("Record inserted successfully into TRADINGHOOK.DB table ", cursor.rowcount)
    cursor.close()
    
# ------------------------------
    
def init_accountbalance_one():
    account = { "userid": 1, "fundid": 1, "exchangeid": 1, "settled": 1000.00, "unsettled": 0.0}
    insert_into_accountbalance(account)

# ------------------------------

def transactions_to_df(data):
  out = {}
  df1 = pandas.DataFrame(out, columns = ['userid', 'symbol','side', 'qty', 'price', 'orderplaced', 'orderfilled'])  
  for row in data:
    userid = {"userid": row[0]}
    symbol = {"symbol": row[1]}
    side = {"side": row[2]}
    qty = {"qty": row[3]}
    price = {"price": row[4]}
    orderplaced = {"orderplaced": row[5]}
    orderfilled = {"orderfilled": row[6]}
    bar = {**userid, **symbol, **side, **qty, **price, **orderplaced, **orderfilled}
    df1 = df1.append(bar,ignore_index=True)
  return (df1)

# -------------------------------------------------------------------
    
def list_to_df(data):
  out = {}
  df1 = pandas.DataFrame(out, columns = ['time', 'ticker', 'qty', 'price','amount'])  
  for row in data:
    date = {"time": row[0]}
    ticker = {"ticker": row[1]}
    qty = {"qty": row[2]}
    price = {"price": row[3]}
    amount = {"amount": row[4]}
    bar = {**date, **ticker, **qty, **price, **amount}
    df1 = df1.append(bar,ignore_index=True)
  return (df1)    
  
# ---------------------------------------------------------------------------

def add_position(trade):
    print("TRADINGHOOK.ADD_POSITION: [ENTER]")
    print(trade)
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        sqlite_insert_query = ("INSERT INTO position (time,ticker,qty,price,amount)\n" +
                               "VALUES(\""+trade['time']+"\"," +
                               "\""+trade['ticker']+"\","+
                               "\""+"1"+"\","+
                               "\""+trade['close']+"\","+
                               "\""+"1"+"\")")
        cursor = conn.cursor()
        count = cursor.execute(sqlite_insert_query)
        conn.commit()
        print("Record inserted successfully into table POSITION:", cursor.rowcount)
        cursor.close()
    else:
        print("oops4")    
    print("TRADINGHOOK: [EXIT]")

# ---------------------------------------------------------------------------

def record_transaction(transaction):
    print("TRADINGHOOK.RECORD_TRANSACTION: [ENTER]")
    print(trade)
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        sqlite_insert_query = ("INSERT INTO transactions (userid,symbol,side,qty,price,orderplaced,orderfilled)\n" +
                               "VALUES(\""+transaction['userid']+"\"," +
                               "\""+transaction['symbol']+"\"," +
                               "\""+transaction['side']+"\","+
                               "\""+transaction['qty']+"\","+
                               "\""+transaction['price']+"\","+
                               "\""+transaction['orderplaced']+"\","+
                               "\""+transaction['orderfilled']+"\");")
        print(sqlite_insert_query)
        cursor = conn.cursor()
        count = cursor.execute(sqlite_insert_query)
        conn.commit()
        print("Record inserted successfully into table POSITION:", cursor.rowcount)
        cursor.close()
    else:
        print("oops4")    
    print("TRADINGHOOK.RECORD_TRANSACTION: [EXIT]")

#-------------------------------------------------------------

def delete_position(x):
    print("TRADERDB.DELETE_POSITION:")
    rows = ""
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        query = ("DELETE FROM position WHERE ticker = '"+x+"';")                             
        cursor = conn.cursor()
        count = cursor.execute(query)
        conn.commit()        
        print ("OUT:",count)
    else:
        print("Error! cannot create the database connection.")
    cursor.close()

# -------------------------------

def return_transactions():
    rows = []
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        query = ("SELECT * FROM transactions WHERE 1=1;")                             
        cursor = conn.cursor()
        count = cursor.execute(query)
        rows = cursor.fetchall() 
        cursor.close()
    else:
        print("Error! cannot create the database connection.")
    return rows

# -------------------------------
 
def webull_exchange_buy(trade):
  print("WEBULL_EXCHANGE_BUY: [ENTER]")
  config = configparser.ConfigParser()
  config.read_file(open('defaults.cfg'))
  username = config['DEFAULT']['username']
  password = config['DEFAULT']['password']
  token = config['DEFAULT']['token']
  #print(username)
  #print(password)
  #print(token)
  #print("POINT1:")
  wb = paper_webull()
  #print("POINT2:")  
  a = wb.login(username, password)
  #print("x:", a)
  #print("POINT3:")    
  a = wb.get_trade_token(token)
  #print("x:", a)
  #print("POINT4:")  
  ticker = trade["ticker"]
  print("ticker:",ticker)  
  amt = float(trade["close"])
  #print("type:", type(amt)) 
  print("amt:", amt)
  #default action = BUY
  #a = wb.place_order(ticker, price=amt, quant=20) 
  print("order status:", a)
  add_position(trade)
  #
  #transaction = Transaction()
  #transaction.userid = 1
  #transaction.symbol = trade["ticker"]
  #transaction.side = "BUY"
  #transaction.qty = 20
  #transaction.price = float(trade["close"])
  #transaction.orderplaced = trade["time"]
  #transaction.orderfilled = "2021-08-13T13:40:00Z" 
  #record_transaction(transaction)
  print("WEBULL_EXCHANGE_BUY: [EXIT]")  
  
# ------------------------------- 
  
def webull_live_buy(trade):
  print("WEBULL_LIVE_BUY: [ENTER]")
  config = configparser.ConfigParser()
  config.read_file(open('defaults.cfg'))
  username = config['DEFAULT']['username']
  password = config['DEFAULT']['password']
  token = config['DEFAULT']['token']
  #print(username)
  #print(password)
  #print(token)
  #print("POINT1:")
  wb = webull()
  #print("POINT2:")  
  a = wb.login(username, password)
  #print("x:", a)
  #print("POINT3:")    
  a = wb.get_trade_token(token)
  #print("x:", a)
  #print("POINT4:")  
  ticker = trade["ticker"]
  print("ticker:",ticker)  
  amt = float(trade["close"])
  #print("type:", type(amt)) 
  print("amt:", amt)
  #default action = BUY
  a = wb.place_order(ticker, price=amt, quant=20) 
  print("order status:", a)
  add_position(trade)
  #transaction = Transaction()
  #transaction.userid = 1
  #transaction.symbol = trade["ticker"]
  #transaction.side = "BUY"
  #transaction.qty = 20
  #transaction.price = float(trade["close"])
  #transaction.orderplaced = trade["time"]
  #transaction.orderfilled = "2021-08-13T13:40:00Z" 
  #record_transaction(transaction)
  print("WEBULL_LIVE_BUY: [EXIT]")    
 
# -------------------------------

def webull_exchange_sell(x):
  print("WEBULL_LIVE_SELL: [ENTER]")
  config = configparser.ConfigParser()
  config.read_file(open('defaults.cfg'))
  username = config['DEFAULT']['username']
  password = config['DEFAULT']['password']
  token = config['DEFAULT']['token']
  #print(username)
  #print(password)
  #print(token)
  wb = paper_webull()
  a = wb.login(username, password)
  #print("x:", a)
  a = wb.get_trade_token(token)
  #print("x:", a)
  a1 = x["ticker"]
  #print("type:", type(a1))
  print("ticker:",a1)  
  amt = float(x["close"])
  #print("type:", type(amt)) 
  print("amt:", amt)
  a = wb.place_order(stock=a1, price=amt, quant=20, action="SELL")
  print("order status:", a)
  delete_position(x["ticker"]) 
  print("WEBULL_LIVE_SELL: [EXIT]")  
  
# -------------------------------

def webull_live_sell(x):
  print("WEBULL_LIVE_SELL: [ENTER]")
  config = configparser.ConfigParser()
  config.read_file(open('defaults.cfg'))
  username = config['DEFAULT']['username']
  password = config['DEFAULT']['password']
  token = config['DEFAULT']['token']
  #print(username)
  #print(password)
  #print(token)
  wb = webull()
  a = wb.login(username, password)
  #print("x:", a)
  a = wb.get_trade_token(token)
  #print("x:", a)
  a1 = x["ticker"]
  #print("type:", type(a1))
  print("ticker:",a1)  
  amt = float(x["close"])
  #print("type:", type(amt)) 
  print("amt:", amt)
  a = wb.place_order(stock=a1, price=amt, quant=20, action="SELL")
  print("order status:", a)
  delete_position(x["ticker"]) 
  print("WEBULL_LIVE_SELL: [EXIT]")    

# -------------------------------

def papertrade_exchange_sell(x):
  '''  username = "x"
  password = "x"
  token = "x"
  tradetool = papertrade()
  a = tradetool.login(username, password)
  a = tradetool.setauthtoken(token)
  a = tradetool.place_order(stock = "x", price=amt, quant=20, action="SELL")
  '''
  return
  
# -------------------------------

def papertrade_exchange_buy(x):
  return
  
# -------------------------------

def log(msg):
  logging.basicConfig(filename="sample.log", level=logging.INFO)
  #logging.debug("This is a debug message")
  logging.info(msg)
  #logging.error("An error has happened!")

# -------------------------------

def trade_buy(trade):
  print("TRADE_BUY:")
  #fname = "config.ini"
  #config = configparser.ConfigParser()
  #config.read_file(open(fname))
  #balance_str = config['DEFAULT']['balance']
  #balance = float(balance_str)
  #print("balance", balance)
  #delta = trade["close"]
  #balance -= float(delta)
  #balance_str = str(balance)
  #config.set('DEFAULT', 'balance', balance_str)
  #save the file
  #with open(fname, 'w') as configfile:
  #  config.write(configfile)
  log("buy: " + trade["ticker"] + " " + trade["close"])
  # make decision
  # webull_exchange_buy(trade)
  webull_live_buy(trade)

# -------------------------------
  
def trade_sell(x):
  print("TRADE_SELL: [ENTER]")
  #fname = "config.ini"
  # config = configparser.ConfigParser()
  # config.read_file(open(fname))
  # balance_str = config['DEFAULT']['balance']
  # balance = float(balance_str)
  # print("balance", balance)  
  # delta = x["close"]
  # balance += float(delta)
  # balance_str = str(balance)
  #config.set('DEFAULT', 'balance', balance_str)
  #save the file
  #with open(fname, 'w') as configfile:
  #  config.write(configfile)
  log("sell: " + x["ticker"] + " " + x["close"])
  #webull_exchange_sell(x)
  webull_live_sell(x)

# -------------------------------

def parse(x):
  if (type(x)) is bytes: 
    x = json.loads(x)
  print("----[New Order]----------------------------------")
  #print(type(x))
  #print (x)
  #print ("----")
  time = x["time"]
  ticker = x["ticker"]
  action = x["order_action"]
  close = x["close"]
  print(Fore.MAGENTA + Style.BRIGHT + time + " " + ticker + " " + action + " " + close + Style.RESET_ALL)

  if action == "buy":
    trade_buy(x)
  elif action =="sell":
    q = have_position(x["ticker"])
    if q == True:
      trade_sell(x)
    else:
      print("attempted to Sell something we do not have a positon on and we DO NOT have MARGINS enabled")
  #
  print("ENDPARSE:")  
  
# -------------------------------
  
def init_tradecode():
    logging.info("tradecode_init()")
    if !is_present("transactions"):
        logging.info("creating transactions table.")
        create_transactions_table() 
    
    create_position_table()
    create_transactions_table() 
    create_accountbalance()
    create_transactions_table()    