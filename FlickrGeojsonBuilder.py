from GeojsonBuilder import GeojsonBuilder

class FlickrGeojsonBuilder (GeojsonBuilder):
	
	def build_geojson(self, loaded_json):
		features = []
		for photo in loaded_json:
			properties = {
				'source':'Flickr',
				'title':photo['title'],
				'datetaken':photo['datetaken'],
				'tags':photo['tags']			
			}
			feature = self.build_feature(photo['longitude'], photo['latitude'], properties)
			features.append(feature)
		return self.build_feature_collection(features)