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
from app.common_db import is_table_present 

# ------------------------------

class AccountBalance:
    def __init__(self):
      self.userid = 0
      self.fundid = 0
      self.exchangeid = 0
      self.settled = 0
      self.unsettled = 0

class ExchangeAccount:
    def __init__(self):
      self.InstanceID = 0
      self.UserID = 0
      self.ExchangeID = 0
      self.exchangenickname = ""
      self.exchangeusername = ""
      self.exchangepassword = ""      
      self.exchangetoken = ""
      
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
    account = AccountBalance()
    for row in cursor:
      account.userid = int(row[0])
      account.fundid = int(row[1])
      account.exchangeid = int(row[2])
      account.settled = float(row[3])
      account.unsettled = float(row[4])
    return account

# -----------

def query_account(accountid):
    conn = create_connection(CONFIG.DATABASE)
    #print(fundid)
    #print(type(fundid))
    sqlite_statement = ("SELECT * FROM accounts WHERE accountid = \""+str(accountid)+"\";")
    #print(sqlite_statement)
    cursor = conn.execute(sqlite_statement)
    account = Account()
    for row in cursor:
      account.exchangeid = int(row[0])
      account.fundid = int(row[1])
      account.exchangeid = int(row[2])
      account.settled = float(row[3])
      account.unsettled = float(row[4])
    return account

# ------------------------------

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# ------------------------------

def have_position(x):
    rows = []
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        query = ("SELECT * FROM position WHERE symbol = '"+x+"';")                             
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

# ------------------------------

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

# ------------------------------

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# ------------------------------
    
def create_accountbalance():
    sql_statement = """ CREATE TABLE IF NOT EXISTS accountbalance (
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
        create_table(conn, sql_statement)
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
    sql_statement = """ CREATE TABLE IF NOT EXISTS position (
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
        create_table(conn, sql_statement)
    else: 
        print("Error! cannot create the database connection.")
        
# ------------------------------

def create_trades_table():    
    sql_statement = """ CREATE TABLE IF NOT EXISTS trades (
                           date text,
                           ticker text,
                           qty  text,   
                           side text,
                           lim text,
                           price  text,
                           amount text
                        ); """
    # create a database connection
    conn = create_connection(CONFIG.DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, sql_statement)
    else: 
        print("Error! cannot create the database connection.")
        
# ------------------------------

def create_conditions_table():    
    sql_statement = """ CREATE TABLE IF NOT EXISTS conditions (
                           InstanceID text,
                           UserID text,
                           ExchangeID text,
                           exchangenickname text,
                           exchangeusername  text,   
                           exchangepassword text,
                           exchangetoken text
                        ); """
    # create a database connection
    conn = create_connection(CONFIG.DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, sql_statement)
    else: 
        logging.info("[CREATE_CONDITIONS]Error! cannot create the database connection..")


# ------------------------------

def create_exchangeaccounts_table():    
    sql_statement = """ CREATE TABLE IF NOT EXISTS exchangeaccounts (
                           InstanceID text,
                           UserID text,
                           ExchangeID text,
                           exchangenickname text,
                           exchangeusername  text,   
                           exchangepassword text,
                           exchangetoken text
                        ); """
    # create a database connection
    conn = create_connection(CONFIG.DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, sql_statement)
    else: 
        print("Error! cannot create the database connection.")
        
 # ------------------------------

def insert_into_ExchangeAccount(exaccount):
    conn = create_connection(CONFIG.DATABASE)
    sqlite_statement = ("INSERT INTO exchangeaccounts (InstanceID,UserID,ExchangeId," +
                           "exchangenickname,exchangeusername,exchangepassword,exchangetoken)\n" +
                           "VALUES(\""+str(exaccount.InstanceID)+"\"," +
                             "\""+str(exaccount.UserID)+"\","+
                             "\""+str(exaccount.ExchangeID)+"\","+
                             "\""+str(exaccount.exchangenickname)+"\","+
                             "\""+str(exaccount.exchangeusername)+"\","+
                             "\""+str(exaccount.exchangepassword)+"\","+
                             "\""+str(exaccount.exchangetoken)+"\");")
    cursor = conn.cursor()
    count = cursor.execute(sqlite_statement)
    conn.commit()
    cursor.close()

# ------------------------------ 

def query_ExchangeAccount(InstanceID):
    conn = create_connection(CONFIG.DATABASE)
    sql_statement = ("SELECT * FROM exchangeaccounts WHERE InstanceID = \""+str(InstanceID)+"\";")
    cursor = conn.execute(sql_statement)
    exchangeaccount = ExchangeAccount()
    for row in cursor:
      exchangeaccount.InstanceID = int(row[0])
      exchangeaccount.UserID = int(row[1])
      exchangeaccount.ExchangeID = int(row[2])
      exchangeaccount.exchangenickname = row[3]
      exchangeaccount.exchangeusername = row[4]
      exchangeaccount.exchangepassword = row[5]
      exchangeaccount.exchangetoken = row[6]
    return exchangeaccount

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

# ------------------------------
    
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
  
# ------------------------------

def add_position(trade):
    logging.info("TRADINGHOOK.ADD_POSITION: [ENTER]")
    #print(trade)
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        sql_statement = ("INSERT INTO position (time,symbol,qty,price,amount)\n" +
                               "VALUES(\""+trade['time']+"\"," +
                               "\""+trade['ticker']+"\","+
                               "\""+"1"+"\","+
                               "\""+trade['close']+"\","+
                               "\""+"1"+"\")")
        cursor = conn.cursor()
        count = cursor.execute(sql_statement)
        conn.commit()
        logging.info("Record inserted successfully into table POSITION: {}".format(cursor.rowcount))
        cursor.close()
    else:
        logging.info("oops4")    
    logging.info("TRADINGHOOK: [EXIT]")

# ------------------------------

def record_transaction(transaction):
    logging.info("TRADINGHOOK.RECORD_TRANSACTION: [ENTER]")
    #print(trade)
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        sql_statment = ("INSERT INTO transactions (userid,symbol,side,qty,price,orderplaced,orderfilled)\n" +
                               "VALUES(\""+transaction['userid']+"\"," +
                               "\""+transaction['symbol']+"\"," +
                               "\""+transaction['side']+"\","+
                               "\""+transaction['qty']+"\","+
                               "\""+transaction['price']+"\","+
                               "\""+transaction['orderplaced']+"\","+
                               "\""+transaction['orderfilled']+"\");")
        logging.info(sql_statement)
        cursor = conn.cursor()
        count = cursor.execute(sql_statement)
        conn.commit()
        logging.info("Record inserted successfully into table POSITION: {}".format(cursor.rowcount))
        cursor.close()
    else:
        logging.info("oops4")    
    logging.info("TRADINGHOOK.RECORD_TRANSACTION: [EXIT]")

# ------------------------------

def delete_position(x):
    logging.info("TRADERDB.DELETE_POSITION:")
    rows = ""
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        query = ("DELETE FROM position WHERE symbol = '"+x+"';")                             
        cursor = conn.cursor()
        count = cursor.execute(query)
        conn.commit()        
        logging.info("OUT: {}".format(count))
    else:
        logging.info("Error! cannot create the database connection.")
    cursor.close()

# ------------------------------

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
 
def paperwebull_buy(trade):
  logging.info("PAPERWEBULL_BUY: [ENTER]")
  ea = query_ExchangeAccount(1)    
  wb = paper_webull()
  a = wb.login(ea.exchangeusername,ea.exchangepassword)
  a = wb.get_trade_token(ea.exchangetoken)
  ticker = trade["ticker"]
  print("ticker:",ticker)  
  amt = float(trade["close"])
  #print("type:", type(amt)) 
  print("amt:", amt)
  #default action = BUY
  #a = wb.place_order(ticker, price=amt, quant=20) 
  print("order status:", a)
  add_position(trade)
  logging.info("PAPERWEBULL_BUY: [EXIT]")  
  
# ------------------------------- 
#   def place_order_otoco(self, stock='', price='', stop_loss_price='', limit_profit_price='', time_in_force='DAY', quant=0) :
  
def webull_live_buy(trade):
    logging.info("WEBULL_LIVE_BUY: [ENTER]")
    ea = query_ExchangeAccount(2)    
    wb = webull()
    a = wb.login(ea.exchangeusername, ea.exchangepassword)
    a = wb.get_trade_token(ea.exchangetoken)
    logging.info("token_status: {}".format(a))
    symbol = trade["ticker"]
    logging.info("symbol: {} ".format(symbol))  
    price = float(trade["close"])
    qty = 20
    limit_profit = price + 0.30 
    stop_loss = price - (price * 0.07)
    stop_loss = round(stop_loss,2)
    logging.info("stop_loss: {}".format(string(stop_loss)))    
    #a = wb.place_order(ticker, price=amt, quant=20) 
    a = wb.place_order_otoco(symbol, price=price, stop_loss_price=stop_loss, limit_profit_price=limit_profit, time_in_force='DAY', quant=qty) 
    logging.info("order status: {}".format(a))
    add_position(trade)
    logging.info("WEBULL_LIVE_BUY: [EXIT]")    
 
# -------------------------------

def paperwebull_sell(x):
    logging.info("PAPERWEBULL_SELL: [ENTER]")
    ea = query_ExchangeAccount(2)
    wb = paper_webull()
    a = wb.login(username, password)
    a = wb.get_trade_token(token)
    a1 = x["ticker"]
    print("ticker:",a1)  
    amt = float(x["close"])
    print("amt:", amt)
    a = wb.place_order(stock=a1, price=amt, quant=20, action="SELL")
    print("order status:", a)
    delete_position(x["ticker"]) 
    logging.info("PAPERWEBULL_SELL: [EXIT]")  
  
# -------------------------------

def webull_live_sell(x):
    logging.info("WEBULL_LIVE_SELL: [ENTER]")
    ea = query_ExchangeAccount(2)
    wb = webull()
    a = wb.login(ea.exchangeusername, ea.exchangepassword)
    a = wb.get_trade_token(ea.exchangetoken)
    a1 = x["ticker"]
    amt = float(x["close"])
    a = wb.place_order(stock=a1, price=amt, quant=20, action="SELL")
    logging.info("order status: {}".format(a))
    delete_position(x["ticker"]) 
    logging.info("WEBULL_LIVE_SELL: [EXIT]")    

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
  logging.info("TRADE_BUY:")
  # paperwebull_buy(trade)
  webull_live_buy(trade)

# -------------------------------
  
def trade_sell(x):
  logging.info("TRADE_SELL: [ENTER]")
  #paperwebull_sell(x)
  #webull_live_sell(x)

# -------------------------------

def parse(x):
    if (type(x)) is bytes: 
        x = json.loads(x)
        logging.info("----[New Order]----------------------------------")
        time = x["time"]
        ticker = x["ticker"]
        action = x["order_action"]
        close = x["close"]

        logging.info("parse()")
        logging.info("time:{}".format(time))
        logging.info("symbol:{}".format(ticker))
        logging.info("action:{}".format(action))
        logging.info("price:{}".format(close))
  
        if action == "buy":
            trade_buy(x)
        elif action =="sell":
            q = have_position(x["ticker"])
            if q == True:
                trade_sell(x)
            else:
                logging.info("attempted to Sell something we do not have a positon on and we DO NOT have MARGINS enabled")
  
# -------------------------------
  
def init_tradecode():
    logging.info("tradecode_init()")
    if not is_table_present("transactions"):
        logging.info("creating transactions table.")
        create_transactions_table() 
    
    if not is_table_present("position"):  
        logging.info("creating position table.")
        create_position_table()
      
    if not is_table_present("accountbalance"):
        logging.info("creating accountbalance table.")
        create_accountbalance()

    if not is_table_present("trades"):
        logging.info("creating trades table.")
        create_trades_table()    
        
    if not is_table_present("exchangeaccounts"):
        logging.info("creating exchangeaccounts table.")
        create_exchangeaccounts_table()     

    if not is_table_present("conditions"):
        logging.info("creating conditions table.")
        create_conditions_table()    
