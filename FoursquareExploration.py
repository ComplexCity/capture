from FoursquareDatabaseManager import FoursquareDatabaseManager
from LoggerBuilder import LoggerBuilder
import logging
import sqlite3
import json


f = open("foursquare/shanghai/foursquare-shanghai-sections-14-04-14.json", 'r')
data = f.read()
venues = json.loads(data)
f.close()

db_conn = sqlite3.connect('foursquare/foursquare.db')
db_cursor = db_conn.cursor()
db_manager = FoursquareDatabaseManager(None)

db_manager.load_venues(db_cursor, venues, 'VenueToExplore2')

db_conn.commit()
db_conn.close()