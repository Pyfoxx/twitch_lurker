import os

import psycopg2
from psycopg2 import sql

conn = None


def connect(db, user, passwd, ip="127.0.0.1"):
	"""
	Connects to the PostgreSQL database.

	:return: The database connection object.
	"""
	global conn
	print('Connecting to the PostgreSQL database...')
	conn = psycopg2.connect(database=db, user=user, password=passwd, host=ip)#, host="172.17.0.3"
	print("connected")
	return conn


def select_user():
	"""
	:return: A list of rows containing the selected data.
	"""
	global conn
	print("selecting user")
	to_return = []
	cur = conn.cursor()
	cur.execute(f"SELECT * FROM streamers")

	rows = cur.fetchall()
	print("AAAAAAAAAAAH")

	for row in rows:
		print(row)
		to_return.append(row)


# return to_return


def add_streamer(user_id, username, pp_url, by):
	global conn
	print('add stream to follow function')
	sql = f"INSERT INTO streamers VALUES('{user_id}', '{username}', '{pp_url}', '{by}')"
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()


def del_streamer(str_name):
	global conn
	print('delete stream from follow function')
	sql = f"DELETE FROM streamers WHERE name = '{str_name}'"
	# print(sql)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()


def conf(db, user, passwd, ip="127.0.0.1"):
	connect(db, user, passwd, ip)
	sql = "SELECT tok, twitch_token, db_username, db_passw, db_ip, db_name, guild_id, cmd_chann, stream_chann FROM instances_conf " #where pid = {pid}
	print(sql)
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	print(fetch)
	if fetch:
		return fetch
	else:
		return None

def add_temp_streamer(msg_id, streamer, pid):
	global conn
	print('add stream to follow function')
	sql = f"UPDATE instances_conf SET temp_streamer = '{streamer}' WHERE pid = {pid}; \
	UPDATE instances_conf SET temp_streamer_msg = '{msg_id}' WHERE pid = {pid}"
	# print(sql)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def del_temp_streamer(pid):
	global conn
	print('del stream to follow function')
	sql = (f"UPDATE instances_conf SET temp_streamer = Null WHERE pid = {pid}; \
	UPDATE instances_conf SET temp_streamer_msg = Null WHERE pid = {pid}")
	# print(sql)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def get_temp_streamer(pid):
	global conn
	sql = f"SELECT temp_streamer, temp_streamer_msg FROM instances_conf WHERE pid = {pid}"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return fetch[0]
	else:
		return None


def get_streamers_ids():
	global conn
	sql = f"SELECT id FROM streamers"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return [i[0] for i in fetch]
	else:
		return None

def get_streamers_name():
	global conn
	sql = f"SELECT name FROM streamers"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return [i[0] for i in fetch]
	else:
		return []



def get_streams_ids():
	global conn
	sql = f"SELECT streamer_id FROM streams"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return [i[0] for i in fetch]
	else:
		return []

def get_streamer_name_by_id(streamer_id):
	global conn
	sql = f"SELECT name FROM streamers WHERE id = '{streamer_id}'"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return fetch[0][0]
	else:
		return None

def get_streamer_id_by_name(streamer_name):
	global conn
	sql = f"SELECT name FROM streamers WHERE name = '{streamer_name}'"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return fetch[0][0]
	else:
		return None

def was_streaming(id):
	global conn
	sql = f"SELECT * FROM streams WHERE streamer_id = '{id}'"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return fetch[0][0]
	else:
		return None


def add_stream(user_id, id, game_id, name, thumb, lang, mature, msg_id):
	global conn
	print('add stream')
	sql = f"INSERT INTO streams VALUES('{user_id}', '{id}', '{game_id.replace("'", "''")}', '{name.replace("'", "''")}', '{thumb}', '{lang}', '{mature}', '{msg_id}')"
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def get_stream_msg(id):
	global conn
	print('add stream')
	sql = f"SELECT msg_id FROM streams where streamer_id = '{id}'"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return fetch[0][0]
	else:
		return None

def del_stream(user_id):
	global conn
	print('delete stream from follow function')
	sql = f"DELETE FROM streams WHERE streamer_id = '{user_id}'"
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def get_streamer_pp(id):
	global conn
	print('add stream')
	sql = f"SELECT pp FROM streamers where id = '{id}'"
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return fetch[0][0]
	else:
		return None

def get_token(pid):
	global conn
	print('token')
	sql = f'SELECT tok FROM instances_conf where pid = {pid}'
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return fetch[0][0]
	else:
		return None

def get_tw_token(pid):
	global conn
	print('token')
	sql = f'SELECT twitch_token FROM instances_conf where pid = {pid}'
	cur = conn.cursor()
	cur.execute(sql)
	fetch = cur.fetchall()
	if fetch:
		return fetch[0][0]
	else:
		return None