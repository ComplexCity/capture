from GeojsonBuilding import GeojsonBuilding
from FoursquareGeojsonBuilder import FoursquareGeojsonBuilder
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

source = 'foursquare'

def main():
	try:
		GeojsonBuilding(logger, source, FoursquareGeojsonBuilder()).build()
		return 0
		
	except Exception, e:
		logger.critical(e, exc_info=True)
		return 1

if __name__ == "__main__":
	logger.critical("START")
	res = main()
	logger.critical("STOP")
	sys.exit(res)
