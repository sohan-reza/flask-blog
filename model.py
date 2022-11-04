import sqlite3

def db_connect():
	conn = sqlite3.connect('database.db')
	#conn.row_factory = sqlite3.Row
	return conn
	
def insert_usr_data(tbl, data):
	conn = db_connect()
	flag=None
	try:
		d = conn.execute(f"Insert into {tbl} (first_name, last_name, username, password) VALUES {data}")
		conn.commit()
		flag = d.rowcount
	except:
		pass
	conn.close()
	return flag
	

def fetch_usr(usr):
	conn = db_connect()
	usr_list = conn.execute(f"SELECT * FROM users WHERE username='{usr}'").fetchall()
	conn.close()
	
	if usr_list:
		return usr_list[0]
	return None
	
	


def put_post(data):
	conn = db_connect()
	flag=None
	try:
		d = conn.execute(f"INSERT INTO `posts` (title, description, author) VALUES {data}")
		conn.commit()
		flag = d.rowcount
	except:
		pass
	conn.close()
	return flag 


def fetch_post():
	conn = db_connect()
	d={}
	flag=None
	try:
		conn.row_factory = sqlite3.Row
		d = conn.execute(f"SELECT id, title, description, author, date FROM posts order by date DESC").fetchall()
		
	except:
		flag=True
	conn.close()
	if flag == None:
		return d
	return None 


def fetch_usr_post(usrname):
	conn = db_connect()
	d={}
	flag=None
	try:
		conn.row_factory = sqlite3.Row
		d = conn.execute(f"SELECT * FROM posts where author='{usrname}' order by date DESC").fetchall()
		
	except:
		flag=True
	conn.close()
	if flag == None:
		return d
	return None
	
def delete_post(id):
	conn = db_connect()
	x=0
	try:
		conn.execute(f"Delete FROM posts where id={id}")
		conn.commit()
		x=-1
	except:
		x=1
	conn.close()
	return x
	

def up_post(data):
	conn = db_connect()
	flag=None
	try:
		d = conn.execute(f"UPDATE posts set title='{data[0]}', description='{data[1]}' where id={data[2]}")
		conn.commit()
		flag = d.rowcount
	except:
		pass
	conn.close()
	return flag 


def update_profile(f, l, pa, username):
	conn = db_connect()
	flag=None
	try:
		
		d = conn.execute(f"UPDATE users set first_name='{f}', last_name='{l}', password='{pa}' where username='{username}'")
		
		
		conn.commit()
		flag = d.rowcount
	except:
		return "error"
	conn.close()
	return flag 

