from YelpCaptor import YelpCaptor
from YelpDatabaseManager import YelpDatabaseManager
from FileManager import FileManager
from datetime import datetime
from ExitLogger import ExitLogger
from LoggerBuilder import LoggerBuilder
import logging
import sys
import sqlite3

# API terms => http://www.yelp.com/developers/getting_started/api_terms
# Limits: 10,000 calls per day => http://www.yelp.com/developers/documentation/faq
# Errors => http://www.yelp.com/developers/documentation/v2/errors

source = 'yelp'
logger = LoggerBuilder(source, logging.WARNING, logging.INFO).get_logger()
exit_logger = ExitLogger(source)

yelp_db = 'yelp/yelp.db'

def main():
	captor = YelpCaptor(logger)
	file_manager = FileManager()
	
	try:
		cities = file_manager.get_locations(source)
		
		db_conn = sqlite3.connect(yelp_db)
		db_cursor = db_conn.cursor()
		db_manager = YelpDatabaseManager(logger)
		
		my_cities = exit_logger.read_back_file()
		if len(my_cities) == 0:
			my_cities = cities
		remaining_locations = my_cities.copy()
		
		now = datetime.now()
		for city, locations in my_cities.iteritems():
			nb_total_locations = len(cities[city])
			logger.warning("Capting for %s" % city)
			
			for location in locations:
				loaded_json = captor.get_data(location)
				if len(loaded_json) > 0:
					db_manager.insert_venues(db_cursor, loaded_json)
					db_conn.commit()
				remaining_locations[city].remove(location)
				
				nb_locations = nb_total_locations - len(remaining_locations[city])
				logger.warning("%d locations done over %d locations for %s"% (nb_locations, nb_total_locations, city))

			venues = db_manager.get_venues(db_cursor)
			nb_venues = len(venues)
			if nb_venues > 0:
				file_manager.write_json(venues, source, city, now.strftime('%y-%m-%d'))
				logger.warning("New JSON written for %s: %d venues"% (city, nb_venues))
				db_manager.delete_all_venues(db_cursor)
				db_conn.commit()

			remaining_locations.pop(city)
		
		db_conn.close()
		exit_logger.write_back_file(None)
		return 0
		
	except Exception, e:
		logger.critical(e, exc_info=True)
		return 1

		
if __name__ == "__main__":
	start = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	logger.critical("START")
	res = main()
	logger.critical("STOP")
	stop = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	ExitLogger(source).log(start, stop, res)
	sys.exit(res)