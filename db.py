import sqlite3
import time

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS user (
                uid INTEGER
            )''')
con.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS ustatus (
                uid INTEGER,
                status TEXT
            )''')
con.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS ulang (
                uid INTEGER,
                lang TEXT
            )''')
con.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS channels (
                uid INTEGER,
                cid INTEGER,
                uname TEXT
            )''') #IBA - if bot admin
con.commit()



#USER
def add_user(uid):
    cur.execute(f'INSERT INTO user VALUES ({uid})')
    con.commit()

def check_user(uid):
    cur.execute(f'SELECT * FROM user WHERE uid = {uid}')
    user = cur.fetchone()
    if user:
        return True
    return False

#STATUS
def set_status(uid, status):
    cur.execute(f'INSERT INTO ustatus VALUES (?, ?)', (uid, status))
    con.commit()

def upd_status(uid, status):
    cur.execute(f'UPDATE ustatus SET status = ? WHERE uid = ?', (status, uid,))
    con.commit()

def get_status(uid):
    cur.execute(f'SELECT status FROM ustatus WHERE uid = {uid}')
    status = cur.fetchone()[0]
    return status

#LANG
def set_lang(uid, lang):
    cur.execute(f'INSERT INTO ulang VALUES (?, ?)', (uid, lang))
    con.commit()

def upd_lang(uid, lang):
    cur.execute(f'UPDATE ulang SET lang = ? WHERE uid = ?', (lang, uid,))
    con.commit()

def get_lang(uid):
    cur.execute(f'SELECT lang FROM ulang WHERE uid = {uid}')
    lang = cur.fetchone()[0]
    return lang


#channel
def set_channel(uid, cid, iba):
    cur.execute(f'INSERT INTO channels VALUES (?, ?, ?)', (uid, cid, iba))
    con.commit()

def upd_channel_cid(uid, cid):
    cur.execute(f'UPDATE channels SET cid = ? WHERE uid = ?', (cid, uid,))
    con.commit()

def upd_channel_iba(uid, uname):
    cur.execute(f'UPDATE channels SET uname = ? WHERE uid = ?', (uname, uid,))
    con.commit()

def get_channel_cid(uid):
    cur.execute(f'SELECT cid FROM channels WHERE uid = {uid}')
    cid = cur.fetchall()
    return cid

def get_channel_uname(uid):
    cur.execute(f'SELECT uname FROM channels WHERE uid = {uid}')
    uname = cur.fetchone()[0]
    return uname

#Get users
def get_all():
    cur.execute(f'SELECT * from user')
    results = cur.fetchall()
    return results