from FoursquareCaptor import FoursquareCaptor
from FoursquareDatabaseManager import FoursquareDatabaseManager
from FileManager import FileManager
from datetime import datetime
from ExitLogger import ExitLogger
from LoggerBuilder import LoggerBuilder
import logging
import sys
import sqlite3
import requests

# Limits = 5000 calls/h => https://developer.foursquare.com/overview/ratelimits

source = 'foursquare'
logger = LoggerBuilder(source, logging.WARNING, logging.INFO).get_logger()
exit_logger = ExitLogger(source)

foursquare_db = "foursquare"

class InitError(Exception):
	pass

def main():
	return_value = 0

	captor = FoursquareCaptor(logger)
	file_manager = FileManager()

	db_conn = None
	try:
		db_conn = sqlite3.connect(file_manager.get_path(source, None, foursquare_db, ".db"))
		db_cursor = db_conn.cursor()
		db_manager = FoursquareDatabaseManager(logger)
		try:
			cities = file_manager.get_locations(source)
		except IOError:
			raise InitError("File %s is missing"% file_manager.get_locations_path(source))
		except ValueError:
			raise InitError("The %s file does not contain any correct JSON object"% file_manager.get_locations_path(source))
		
		
		my_cities = exit_logger.read_back_file()
		if len(my_cities) == 0:
			my_cities = cities
		remaining_locations = my_cities.copy()
		
		now = datetime.now()
		for city, locations in my_cities.iteritems():
			nb_total_locations = len(cities[city])
			logger.warning("Capting for %s" % city)
			
			for location in locations:
#				loaded_json = captor.get_explore_data(location, now.strftime('%Y%m%d'), False)
#				loaded_json = captor.get_explore_data(location, now.strftime('%Y%m%d'), True)
				loaded_json = captor.get_explore_data_with_sections(location, now.strftime('%Y%m%d'), True)
				
				if len(loaded_json) > 0:
					db_manager.insert_venues(db_cursor, loaded_json)
					db_conn.commit()
				
				remaining_locations[city].remove(location)
				nb_locations = nb_total_locations - len(remaining_locations[city])
				logger.warning("%d locations done over %d locations for %s"% (nb_locations, nb_total_locations, city))

			venues = db_manager.get_venues(db_cursor)
			nb_venues = len(venues)
			if nb_venues > 0:
				try:
					file_manager.write_json(venues, source, city, now.strftime('%y-%m-%d'))
				except IOError:
					raise InitError("Folder %s is missing"% file_manager.get_folder_path(source, city))
				logger.warning("New JSON written for %s: %d venues"% (city, nb_venues))

				db_manager.delete_all_venues(db_cursor)
				db_conn.commit()

			remaining_locations.pop(city)
		
		exit_logger.write_back_file(None)
	
	except InitError as e:
		logger.critical("%s: %s"% (type(e).__name__, e))
		return_value = 1	
	except requests.exceptions.RequestException as e:
		logger.critical("%s: %s"% (type(e).__name__, e))
		exit_logger.write_back_file(remaining_locations)
		return_value = 2
	except FoursquareCaptor.FoursquareApiError as e:
		logger.critical("%s: %s"% (type(e).__name__, e))
		exit_logger.write_back_file(remaining_locations)
		return_value = 3
	except sqlite3.OperationalError as e:
		logger.critical("SQLite3 %s: %s"% (type(e).__name__, e))
		return_value = 4
	except Exception as e:
		logger.critical(e, exc_info=True)
		exit_logger.write_back_file(remaining_locations)
		return_value = 5
	finally:
		if db_conn<> None:
			db_conn.close()
		return return_value

if __name__ == "__main__":
	start = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	logger.critical("START")
	res = main()
	logger.critical("STOP (%d)"% res)
	stop = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	exit_logger.log(start, stop, res)
	sys.exit(res)
		