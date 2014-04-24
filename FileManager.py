import json

class FileManager:
	def get_path(self, source, city, filename, extension='.json'):
		if city <> None:
			return "./" + source.lower() + "/" + city.lower() + "/" + filename + extension
		return "./" + source.lower() + "/" + filename + extension
	
	def get_locations(self, source):
		path = self.get_path(source, None, "locations")
		f = open(path, 'r')
		loaded_json = json.load(f)
		f.close()
		return loaded_json
	
	def write_json(self, loaded_json, source, city, filename):
		path = self.get_path(source, city, filename, ".json")
		f = open(path, 'w')
		json.dump(loaded_json, f)
		f.close()
			
	def write_geojson(self, loaded_json, source, city, filename):
		path = self.get_path(source, city, filename, ".geojson")
		f = open(path, 'w')
		json.dump(loaded_json, f)
		f.close()
				
	def write_js_geojson(self, loaded_geojson, source, city, filename):
		path = self.get_path(source, city, filename, ".js")
		f = open(path, 'w')
		js_geojson = "var geojsonData = %s;"% json.dumps(loaded_geojson)
		f.write(js_geojson)
		f.close()
					
