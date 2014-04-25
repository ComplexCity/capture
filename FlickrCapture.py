from FlickrCaptor import FlickrCaptor
from FileManager import FileManager
from datetime import datetime, timedelta
from time import sleep
import json
from LoggerBuilder import LoggerBuilder
from ExitLogger import ExitLogger
import logging
import os
import sys
import requests

source = 'flickr'
logger = LoggerBuilder(source, logging.WARNING, logging.INFO).get_logger()
# Limit for Flickr API calls: 3600 queries / h (http://www.flickr.com/services/developer/api/)
# Limit for flickr.photos.search: Flickr will return at most the first 4,000 results for any given search query.

# min_date should be written using the YYYY-MM-DD format
min_date_file = "./" + source.lower() + "/min_date.json"
min_date_format = '%Y-%m-%d'

class InitError(Exception):
	pass

def get_min_date():
	if os.path.isfile(min_date_file):
		try:
			f = open(min_date_file, 'r')
			loaded_json = json.load(f)
			f.close()
			min_date = datetime.strptime(loaded_json['min_date'], min_date_format)
		except (ValueError, KeyError):
			raise InitError("You need to set {\"min_date\":\"YYYY-MM-DD\"} in file %s"% min_date_file)
		return min_date
	raise InitError("File %s not found. You should create this file and set {'min_date':YYYY-MM-DD} in it."% min_date_file)
	
def set_min_date(new_min_date):
	f = open(min_date_file, 'w+')
	json.dump({'min_date':new_min_date.strftime(min_date_format)}, f)
	f.close()


def main():	
	last_date = datetime.now() - timedelta(days=2)

	captor = FlickrCaptor(logger)
	file_manager = FileManager()
	
	try:
		woe_ids = file_manager.get_locations(source)
		
		min_date = get_min_date()
		zero_day = timedelta(days=0) 
		one_day = timedelta(days=1)

		if (last_date - min_date) < zero_day:
			raise InitError("The date set as min_date in %s should not be after 2 days ago."% min_date_file)
		while (last_date - min_date) >= zero_day:
			logger.warning("---- Capting for %s" % min_date.strftime('%y-%m-%d'))
			for city, woe_id in woe_ids.iteritems():
				max_date = min_date + one_day
				logger.warning("Capting for %s" % city)
				loaded_json = captor.get_data(min_date, max_date, woe_id)
				file_manager.write_json(loaded_json, source, city, min_date.strftime('%y-%m-%d'))
				logger.warning("New JSON written for %s " % city)
			
			min_date = max_date
			set_min_date(min_date)
			logger.warning("... Sleeping for 5 s")
			sleep(5)
		return 0
		
	except InitError as e:
		logger.critical("%s: %s"% (type(e).__name__, e))
		return 1	
	except requests.exceptions.RequestException as e:
		logger.critical("%s: %s"% (type(e).__name__, e))
		return 2
	except FlickrCaptor.FlickrApiError as e:
		logger.critical("%s: %s"% (type(e).__name__, e))
		return 3
	except Exception as e:
		logger.critical(e, exc_info=True)
		return 4

if __name__ == "__main__":
	start = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	logger.critical("START")
	res = main()
	logger.critical("STOP (%d)"% res)
	stop = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	ExitLogger(source).log(start, stop, res)
	sys.exit(res)