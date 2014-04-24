import json

class YelpDatabaseManager:
	
	def __init__(self, logger):
		self.logger = logger
	
	def insert_venues(self, db_cursor, venues):
		params = []
		for venue in venues:
			params.append((venue['id'], json.dumps(venue)))
		db_cursor.executemany('replace into Venue (id, json) values (?, ?)', params)
		
	def get_venues(self, db_cursor):
		venues = []
		for row in db_cursor.execute('select json from Venue'):
			venue = json.loads(row[0])
			venues.append(venue)
		return venues
		
	def delete_all_venues(self, db_cursor):
		db_cursor.execute('delete from Venue')
