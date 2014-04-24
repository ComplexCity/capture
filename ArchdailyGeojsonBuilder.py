from GeojsonBuilder import GeojsonBuilder

class ArchdailyGeojsonBuilder (GeojsonBuilder):

	def build_geojson(self, loaded_json):
		features = []
		for location in loaded_json:
			properties = {
				'source':'Archdaily',
				'title':location['title'],
				'href':location['href'],
				'src':location['src'],
				'address':location['address']
			}
			feature = self.build_feature(location['lng'], location['lat'], properties)
			features.append(feature)
		return self.build_feature_collection(features)
		
