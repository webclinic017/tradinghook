import sqlite3
import config as CONFIG
import logging

def is_present(table):
    conn = sqlite3.connect(CONFIG.DATABASE)
    c = conn.cursor()
    try:
        query = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='''+table+''';'''
        print(query)
        c.execute(query)
        if c.fetchone()[0]==1 :   
            found = True
            logging.info("x1")
        else: 
            found = False  
            logging.info("x2")
    except:
        found = False
        logging.info("x3")
  
    return (found)