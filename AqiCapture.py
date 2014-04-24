from AqiCaptor import AqiCaptor
from FileManager import FileManager
from LoggerBuilder import LoggerBuilder
from ExitLogger import ExitLogger
import logging
from datetime import datetime
import sys

source = 'AQI'
logger = LoggerBuilder(source, logging.WARNING, logging.INFO).get_logger()

def main():
	captor = AqiCaptor(logger)
	file_manager = FileManager()

	try:
		locations = file_manager.get_locations(source)
		for city, location in locations.iteritems():
			logger.warning("- Capting for %s"% city)
			my_date = datetime.now().strftime('%y-%m-%d-%H')
			loaded_json = captor.get_data(location)
			file_manager.write_json(loaded_json, source, city, my_date)
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