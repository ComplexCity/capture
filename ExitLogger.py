import json
import os

class ExitLogger:
	
	def __init__(self, source):
		self.path = 'logs/' + source.lower() + '-exit.json'
		self.back_file_path = 'logs/' + source.lower() + '-back.json'
	
	def log(self, start, stop, exit):
		f = open(self.path, 'w')
		json_object = {
			'start': start,
			'stop': stop,
			'exit': exit
		}
		json.dump(json_object, f)
		f.close()
	
	def log_with_params(self, start, stop, exit, params):
		f = open(self.path, 'w')
		json_object = {
			'start': start,
			'stop': stop,
			'exit': exit
		}
		if params <> None and len(params) > 0:
			for key, value in params.iteritems():
				json_object[key] = value
		json.dump(json_object, f)
		f.close()
		
	def write_back_file(self, json_object):
		f = open(self.back_file_path, 'w')
		if json_object <> None:
			json.dump(json_object, f)
		f.close()
		
	def read_back_file(self):
		json_object = {}
		if os.path.isfile(self.back_file_path):
			f = open(self.back_file_path, 'r')
			data = f.read()
			if len(data) > 0:
				json_object = json.loads(data)
			f.close()
		return json_object

