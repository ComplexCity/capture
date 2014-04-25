from AqiCaptor import AqiCaptor
from FileManager import FileManager
from LoggerBuilder import LoggerBuilder
from ExitLogger import ExitLogger
import logging
from datetime import datetime
import sys
import requests

source = 'AQI'
logger = LoggerBuilder(source, logging.WARNING, logging.INFO).get_logger()

class InitError(Exception):
	pass

def main():
	captor = AqiCaptor(logger)
	file_manager = FileManager()

	try:
		try:
			locations = file_manager.get_locations(source)
		except IOError:
			raise InitError("File %s is missing"% file_manager.get_locations_path(source))
		except ValueError:
			raise InitError("The %s file does not contain any correct JSON object"% file_manager.get_locations_path(source))
			
		for city, location in locations.iteritems():
			logger.warning("- Capting for %s"% city)
			my_date = datetime.now().strftime('%y-%m-%d-%H')
			loaded_json = captor.get_data(location)
			try:
				file_manager.write_json(loaded_json, source, city, my_date)
			except IOError:
				raise InitError("Folder %s is missing"% file_manager.get_folder_path(source, city))
		
		return 0

	except InitError as e:
		logger.critical("%s: %s"% (type(e).__name__, e))
		return 1
	except requests.exceptions.RequestException as e:
		logger.critical("%s: %s"% (type(e).__name__, e))
		return 2
	except Exception as e:
		logger.critical(e, exc_info=True)
		return 3
	
if __name__ == "__main__":
	start = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	logger.critical("START")
	res = main()
	logger.critical("STOP (%d)"% res)
	stop = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	ExitLogger(source).log(start, stop, res)
	sys.exit(res)