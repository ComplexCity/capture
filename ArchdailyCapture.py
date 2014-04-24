from ArchdailyCaptor import ArchdailyCaptor
from ArchdailyGeojsonBuilder import ArchdailyGeojsonBuilder
from FileManager import FileManager
from LoggerBuilder import LoggerBuilder
import logging
from ExitLogger import ExitLogger
from datetime import datetime
import sys

source = 'archdaily'
logger = LoggerBuilder(source, logging.WARNING, logging.INFO).get_logger()

def main():
	try:
		logger.warning("Capting Archdaily...")
		
		now = datetime.now().strftime('%y-%m-%d')
		loaded_json = ArchdailyCaptor().get_data()
		
		logger.info("Building the GeoJSON...")
		loaded_geojson = ArchdailyGeojsonBuilder().build_geojson(loaded_json)
		
		logger.info("Writing GeoJSON...")
		file_manager = FileManager()
		file_manager.write_geojson(loaded_geojson, source, None, now)
		file_manager.write_js_geojson(loaded_geojson, source, None, now)
		
		logger.warning("New GeoJSON written for Archdaily: %d locations"% len(loaded_json))
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