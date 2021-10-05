import sqlite3
import os.path
import config as CONFIG
import logging


def is_present():
    conn = sqlite3.connect(CONFIG.DATABASE)
    c = conn.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
    if c.fetchone()[0]==1 :   
       found = True
    else: 
        found = False  
    return (found)


def init_db():
    logging.info("init_db()")
    if (os.path.isfile(CONFIG.DATABASE) != True):
        logging.info("creating users table.")
        create_users_table()
        logging.info("inserting initial user.")
        insert_user(1, "admin", "p@$$w0rd")
    else:            
        if is_present() == False:
            logging.info("creating users table.")
            create_users_table()
            logging.info("inserting initial user.")
            insert_user(1, "admin", "p@$$w0rd")

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_users_table():    
    sql_create_table = """ CREATE TABLE IF NOT EXISTS users (
                           id       int,
                           username text,
                           password text
                           ); """
    # create a database connection
    conn = create_connection(CONFIG.DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, sql_create_table)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")


def insert_user(id, username, password):
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        sqlite_insert_query = ("INSERT INTO users (id,username,password)\n" +
                               "VALUES(\""+str(id)+"\"," +
                               "\""+username+"\"," +
                               "\""+password+"\");")
        print(sqlite_insert_query)
        cursor = conn.cursor()
        count = cursor.execute(sqlite_insert_query)
        conn.commit()
        #print("Record inserted successfully into table POSITION:", cursor.rowcount)
        cursor.close()
    else:
        print("oops.")