import sqlite3
import os.path
import config as CONFIG
import logging
from app.common_db import is_present

# ------------------------------

def init_db():
    logging.info("init_db()")
    logging.info(CONFIG.DATABASE)
    if (os.path.isfile(CONFIG.DATABASE) != True):
        logging.info("creating users table. XXX")
        create_users_table()
        logging.info("inserting initial user.")
        insert_user(1, "admin", "p@$$w0rd")
    else:            
        if is_present('users') == False:
            logging.info("creating users table. YYY")
            create_users_table()
            logging.info("inserting initial user.")
            insert_user(1, "admin", "p@$$w0rd")


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        logging.info(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logging.info(e)


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
        logging.info("Error! cannot create the database connection.")


def insert_user(id, username, password):
    conn = create_connection(CONFIG.DATABASE)
    if conn is not None:
        sqlite_insert_query = ("INSERT INTO users (id,username,password)\n" +
                               "VALUES(\""+str(id)+"\"," +
                               "\""+username+"\"," +
                               "\""+password+"\");")
        cursor = conn.cursor()
        count = cursor.execute(sqlite_insert_query)
        conn.commit()
        cursor.close()