class GeojsonBuilder:
	
	def build_feature(self, lng, lat, properties):
		geometry =  {'type':'Point', 'coordinates':[lng, lat]}
		return {'type':'Feature', 'geometry':geometry, 'properties':properties}
	
	def build_feature_collection(self, features):
		return {'type':'FeatureCollection', 'features':features}
	
	# sub-classes needs to implement this method
	def build_geojson(self, loaded_json):
		return None