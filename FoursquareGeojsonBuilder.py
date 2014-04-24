from GeojsonBuilder import GeojsonBuilder

class FoursquareGeojsonBuilder (GeojsonBuilder):

	def build_geojson(self, venues):
		features = []
		for venue in venues:
			properties = {
				'source':'Foursquare',
				'id':venue['id'],
				'name':venue['name'],
				'category':venue['categories'][0]['name'],
				'specials':venue['specials']['count']
			}
			try:
				properties['address'] = venue['location']['address']
			except KeyError:
				pass
			try:
				properties['cross'] = venue['location']['crossStreet']
			except KeyError:
				pass
			try:
				properties['contact'] = venue['contact']['formatted']
			except KeyError:
				pass
			try:
				properties['hours'] = venue['hours']['status']
			except KeyError:
				pass
			try:
				properties['rating'] = venue['rating']
			except KeyError:
				pass
			try:
				properties['likes'] = venue['likes']['count']
			except KeyError:
				pass
			feature = self.build_feature(venue['location']['lng'], venue['location']['lat'], properties)
			features.append(feature)
		return self.build_feature_collection(features)
		
