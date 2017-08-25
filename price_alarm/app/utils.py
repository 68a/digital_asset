from sqlite3 import *

def open_db(db_file):
    conn = connect(db_file)
    return conn

def close_db(conn):
    conn.close()
    
def read_settings_table(conn):
    c = conn.cursor()
    sql = 'select cny_rate, price_diff_on, price_diff_value from settings'
    c.execute(sql)

    ret = c.fetchall()

    c.close()
    return ret

def update_settings_table(conn, data):
    c = conn.cursor()
    sql = """update settings 
             set cny_rate = ?, 
             price_diff_on = ?, 
             price_diff_value = ?
             """
    c.execute(sql, data)
    conn.commit()

def create_db(db_file):
    sql_create_settings = """ CREATE TABLE IF NOT EXISTS settings (
    id integer PRIMARY KEY,
    cny_rate real NOT NULL,
    price_diff_on booleen NOT NULL,
    price_diff_value real NOT NULL
    ); """
    conn = connect(db_file)
    c = conn.cursor()
    c.execute(sql_create_settings)
    try:
        sql = """insert into settings(
                 id ,
                 cny_rate ,
                 price_diff_on ,
                 price_diff_value  )
                values(0,
                 6.9,
                 1,
                 10.0
                )
           """
        c.execute(sql)
    except:
        print ("insert failed.")
    conn.commit()
    conn.close()
    
