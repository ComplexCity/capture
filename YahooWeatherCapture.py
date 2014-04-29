from YahooWeatherCaptor import YahooWeatherCaptor
from FileManager import FileManager
from datetime import datetime
import dateutil.parser
from ExitLogger import ExitLogger
from LoggerBuilder import LoggerBuilder
import logging
import sys
import os

# How often is the weather information updated => http://help.yahoo.com/l/sg/yahoo/weather/general/weather-06.html
# Limits: ~ 1000 - 2000 calls/h => http://developer.yahoo.com/yql/faq/

source = 'yahooweather'
logger = LoggerBuilder(source, logging.WARNING, logging.INFO).get_logger()

class InitError(Exception):
	pass

def main():
	captor = YahooWeatherCaptor()
	file_manager = FileManager()

	try:
		try:
			woe_ids = file_manager.get_locations(source)
		except IOError:
			raise InitError("File %s is missing"% file_manager.get_locations_path(source))
		except ValueError:
			raise InitError("The %s file does not contain any correct JSON object"% file_manager.get_locations_path(source))
		
		for city, woe_id in woe_ids.iteritems():
			logger.warning("Capting for %s" % city)
			loaded_json = captor.get_data(woe_id)
			
			last_build_date = dateutil.parser.parse(loaded_json['lastBuildDate'])
			date_for_path = last_build_date.strftime('%y-%m-%d-%H-%M')
			
			if os.path.isfile(file_manager.get_path(source, city, date_for_path)):
				logger.warning("Same build date for %s (%s)" % (city, last_build_date))
			else:
				try:
					file_manager.write_json(loaded_json, source, city, date_for_path)
				except IOError:
					raise InitError("Folder %s is missing"% file_manager.get_folder_path(source, city))
				logger.warning("New JSON written for %s %s" % (city, last_build_date))
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