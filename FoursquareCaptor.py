from Captor import Captor
import requests

class FoursquareCaptor(Captor):
	
	url = "https://api.foursquare.com/v2/venues/explore"
	client_id = 'YOUR_CLIENT_ID'
	client_secret = 'YOUR_CLIENT_SECRET'
	limit = 50
	sections = ['food', 'drinks', 'coffee', 'shops', 'arts', 'outdoors', 'sights', 'trending', 'specials', 'nextVenues', 'topPicks']
	
	class FoursquareApiError(Exception):
		pass
	
	def __init__(self, logger):
		self.logger = logger
	
	def __get_only_venues(self, loaded_json):
		venues = []
		for group in loaded_json['response']['groups']:
			for item in group ['items']:
				venues.append(item['venue'])
		return venues
	
	def __request_venues(self, payload):
		r = requests.get(self.url, params=payload, headers=self.headers_anonymous)
		try:
			loaded_json = r.json()
		except:
			r.raise_for_status()
		if r.status_code <> requests.codes.ok:
			error = "[code %d] %s"%(loaded_json['meta']['code'], loaded_json['meta']['errorType'])
			if 'errorDetail' in loaded_json['meta']:
				error += ": %s"% loaded_json['meta']['errorDetail']
			raise self.FoursquareApiError(error)
		return loaded_json
	
	def get_explore_data(self, location, version_date, withNear, section=None):
		payload = {
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'v': version_date,
			'limit': self.limit,
		}
		if withNear:
			payload['near'] = location
		else:
			payload['ll'] = location
			payload['radius'] = 200
		if section <> None:
			payload['section'] = section
		
		loaded_json = self.__request_venues(payload)
		total_results = loaded_json['response']['totalResults']
		self.logger.warning("Total venues: %d"% total_results)
		venues = self.__get_only_venues(loaded_json)
		
		nb_venues = len(venues)
		self.logger.info("%d venues now"% nb_venues)
		could_take_all = False
		if total_results <= self.limit:
			could_take_all = True
		total_results -= nb_venues
		while total_results > 0 and could_take_all == False:
			payload['offset'] = nb_venues
			loaded_json = self.__request_venues(payload)
			new_venues = self.__get_only_venues(loaded_json)
			venues += new_venues
			
			nb_venues = len(venues)
			nb_new_venues = len(new_venues)
			self.logger.info("%d more venues => %d venues now"% (nb_new_venues, nb_venues))
			if total_results <= self.limit:
				could_take_all = True
			else:
				total_results -= nb_new_venues
		
		return venues
		
	def get_explore_data_with_sections(self, location, version_date, withNear):
		venues = []
		for section in self.sections:
			self.logger.warning("Capting for section %s", section)
			venues += self.get_explore_data(location, version_date, withNear, section)
		return venues
