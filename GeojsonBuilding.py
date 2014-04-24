from FileManager import FileManager
import os
import sys
import json


class GeojsonBuilding:

	def __init__(self, logger, source, geojson_builder):
		self.logger = logger
		self.source = source
		self.builder = geojson_builder
		

	def build(self):
		fileManager = FileManager()
		
		cities = [dir for dir in os.listdir(self.source) if os.path.isdir(os.path.join(self.source, dir))]
		for city in cities:
			city_path = os.path.join(self.source, city)
			self.logger.info("%s ..."% city)
			files = [os.path.splitext(os.path.normcase(file))[0] for file in os.listdir(city_path) if os.path.splitext(file)[1] == '.json']
			for file in files:
				json_file = os.path.join(city_path, "%s.json"% file)
				geojson_file = os.path.join(city_path, "%s.geojson"% file)
				js_geojson_file = os.path.join(city_path, "%s.js"% file)
				self.logger.info("%s.json"% file)
				if not os.path.isfile(geojson_file) or not os.path.isfile(js_geojson_file):
					f = open(json_file, 'r')
					loaded_json = json.load(f)
					f.close()
					
					loaded_geojson = self.builder.build_geojson(loaded_json)

					fileManager.write_geojson(loaded_geojson, self.source, city, file)
					self.logger.info(" => %s.geojson"% file)
					
					fileManager.write_js_geojson(loaded_geojson, self.source, city, file)
					self.logger.info(" => %s.js"% file)
