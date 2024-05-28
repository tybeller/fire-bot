import sqlite3 as sql
from sqlite3.dbapi2 import adapters
from discord import message
from db_queries import *

db_file = 'fire.db'


def create_tables():
    conn = sql.connect(db_file)
    conn.execute(CREATE_MESSAGE_TABLE)
    
    conn.commit()
    conn.close()

def message_exists(conn, id):
    cur = conn.cursor()
    cur.execute(MESSAGE_EXISTS, (id,))
    return cur.fetchone()

def handle_reaction_add(reaction):
    conn = sql.connect(db_file)
    cur = conn.cursor()

    msg = reaction.message
    existing_message = message_exists(conn, msg.id)
    if existing_message:
        cur.execute(UPDATE_FIRE_COUNT, (reaction.count(), msg.id,))
    else:
        cur.execute(INSERT_MESSAGE, (msg.id, msg.channel.id, reaction.count,))
    conn.commit()
    conn.close()

def handle_reaction_remove(reaction, cleared):
    conn = sql.connect(db_file)
    cur = conn.cursor()

    msg = reaction.message

    existing_message = message_exists(conn, msg.id)
    if not existing_message:
        conn.rollback()
        conn.close()
        return

    if reaction.count == 0 or cleared:
        cur.execute(DELETE_MESSAGE, (msg.id,))
    else:
        print("mod")
        cur.execute(UPDATE_FIRE_COUNT, (reaction.count(), msg.id,))

    conn.commit()
    conn.close()

def fetch_top_three_messages():
    conn = sql.connect(db_file)
    cur = conn.cursor()

    cur.execute(FETCH_TOP_3)
    top_three = cur.fetchall()
    conn.close()
    
    print(top_three[0][0])
    
    return top_three
