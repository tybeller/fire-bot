import sqlite3 as sql
import datetime
import pickle
from discord import message
from db_queries import *

db_file = 'fire.db'


def create_tables():
    conn = sql.connect(db_file)
    conn.execute(CREATE_MESSAGE_TABLE)
    conn.execute(CREATE_ATTACHMENT_TABLE)
    
    conn.commit()
    conn.close()

def message_exists(conn, id):
    cur = conn.cursor()
    cur.execute(MESSAGE_EXISTS, (id,))
    return cur.fetchone()

def handle_reaction_add(reaction, user):
    conn = sql.connect(db_file)
    cur = conn.cursor()

    msg = reaction.message
    existing_message = message_exists(conn, msg.id)
    if existing_message:
        cur.execute(UPDATE_FIRE_COUNT, (reaction.count(), msg.id,))
    else:
        cur.execute(INSERT_MESSAGE, (msg.id, reaction.count, user.display_name, msg.content, msg.author.display_name, msg.jump_url,))
        for attachment in msg.attachments:
            cur.execute(INSERT_ATTACHMENT, (attachment.id, msg.id, attachment.filename, attachment.url,))
    conn.commit()
    conn.close()

def handle_reaction_remove(reaction, cleared):
    conn = sql.connect(db_file)
    cur = conn.cursor()

    msg = reaction.message

    existing_message = message_exists(conn, msg.id)
    if not existing_message:
        print("does not exist")
        conn.rollback()
        conn.close()
        return

    if reaction.count == 0 or cleared:
        print("del")
        cur.execute(DELETE_MESSAGE, (msg.id,))
        cur.execute(DELETE_ATTACHMENTS, (msg.id,))
        print("deleted")
    else:
        print("mod")
        cur.execute(UPDATE_FIRE_COUNT, (reaction.count(), msg.id,))

    conn.commit()
    conn.close()

