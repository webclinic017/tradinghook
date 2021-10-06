import sqlite3
import config as CONFIG

def is_present(table):
    conn = sqlite3.connect(CONFIG.DATABASE)
    c = conn.cursor()
    try:
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='''+table+''' AND name='users' ''')
        if c.fetchone()[0]==1 :   
            found = True
        else: 
            found = False  
    except:
        found = False
  
    return (found)