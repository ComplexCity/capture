import dateutil.parser

class GitHubDatabaseManager:

	def __init__(self, logger):
		self.logger = logger
		
	def is_there_user_to_complete(self, db_cursor):
		db_cursor.execute('select count(*) from User where complete=0')
		row = db_cursor.fetchone()
		if row[0] > 0:
			return True
		else:
			return False
	
	def get_x_users(self, db_cursor, x):
		params = (x,)
		db_cursor.execute('select id, login from User where complete=0 order by id limit ?', params)
		return db_cursor.fetchall()
		
	def complete_user(self, db_cursor, json):
		try: 
			name = json['name']
		except KeyError:
			name = None
		try:
			company = json['company']
		except KeyError:
			company = None
		try:
			blog = json['blog']
		except KeyError:
			blog = None
		try:
			location = json['location']
		except KeyError:
			location = None
		try:
			if json['hireable'] == True:
				hireable = 1
			else:
				hireable = 0
		except KeyError:
			hireable = None			
		created_at = dateutil.parser.parse(json['created_at'])
		updated_at = dateutil.parser.parse(json['updated_at'])
		params = (name, company, blog, location, hireable, json['public_repos'], json['public_gists'], json['followers'], json['following'], created_at, updated_at, json['id'])
		db_cursor.execute('update User set name=?, company=?, blog=?, location=?, hireable=?, public_repos=?, public_gists=?, followers=?, following=?, created_at=?, updated_at=?, complete=1 where id=?', params)
	
	def complete_error_user(self, db_cursor, id):
		params = (id,)
		db_cursor.execute('update User set complete=1 where id=?', params)
	
	def get_last_id(self, db_cursor):
		db_cursor.execute('select max(id) from User')
		row = db_cursor.fetchone()
		if row[0] == None:
			return 0
		return int(row[0])
		
	def insert_user(self, db_cursor, json):
		params = (json['id'], json['login'], json['type'])
		db_cursor.execute('insert into User (id, login, type, complete) values (?, ?, ?, 0)', params)
		
		
		