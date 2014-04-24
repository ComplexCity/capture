import logging
from logging.handlers import RotatingFileHandler

class LoggerBuilder:
	
	def __init__(self, source, file_handler_level, stream_handler_level):
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
		
		formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
		file_handler = RotatingFileHandler('logs/' + source.lower() + '.log', 'a', 1000000, 1)
		file_handler.setLevel(file_handler_level)
		file_handler.setFormatter(formatter)
		self.logger.addHandler(file_handler)

		stream_handler = logging.StreamHandler()
		stream_handler.setLevel(stream_handler_level)
		self.logger.addHandler(stream_handler)
		
	def get_logger(self):
		return self.logger
