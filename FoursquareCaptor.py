from Captor import Captor
import requests
import json

class FoursquareCaptor(Captor):
	
	url = "https://api.foursquare.com/v2/venues/explore"
	client_id = 'NQAA05J4AY1VC2CF0L5J33BYDD53ON5325VTTLBB2UGR0KI1'
	client_secret = '4ZLLVR4FAOMYFB2GJP5BWAJDZNADSRQ3MTRVD3KWBT2BEJLJ'
	limit = 50
	sections = ['food', 'drinks', 'coffee', 'shops', 'arts', 'outdoors', 'sights', 'trending', 'specials', 'nextVenues', 'topPicks']
	
	def __init__(self, logger):
		self.logger = logger
	
	def __get_only_venues(self, loaded_json):
		venues = []
		for group in loaded_json['response']['groups']:
			for item in group ['items']:
				venues.append(item['venue'])
		return venues
	
	
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
		r = requests.get(self.url, params=payload, headers=self.headers_anonymous)
		r.raise_for_status()
		loaded_json = json.loads(r.text)
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
			r = requests.get(self.url, params=payload, headers=self.headers_anonymous)
			r.raise_for_status()
			loaded_json = json.loads(r.text)
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