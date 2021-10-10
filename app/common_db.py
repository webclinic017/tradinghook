import sqlite3
import config as CONFIG
import logging

def is_present(table):
    conn = sqlite3.connect(CONFIG.DATABASE)
    c = conn.cursor()
    try:
        query = '''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}';'''.format(table)
        c.execute(query)
        if c.fetchone()[0]==1 :   
            found = True
        else: 
            found = False  
    except:
        found = False
    return (found)