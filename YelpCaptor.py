from Captor import Captor
import requests
from requests_oauthlib import OAuth1

class YelpCaptor(Captor):
	
	url = "http://api.yelp.com/v2/search"

	oauth_consumer_key = "YOUR_CONSUMER_KEY"
	oauth_consumer_secret = "YOUR_CONSUMER_SECRET"
	oauth_token = "YOUR_TOKEN"
	oauth_token_secret = "YOUR_TOKEN_SECRET"

	class YelpApiError(Exception):
		pass
		
	def __init__(self, logger):
		self.logger = logger
		
	def __request_api(self, payload):
		auth = OAuth1(self.oauth_consumer_key,
					  client_secret=self.oauth_consumer_secret,
					  resource_owner_key=self.oauth_token,
					  resource_owner_secret=self.oauth_token_secret,
					  signature_type='query')
		r = requests.get(self.url, params=payload, auth=auth, headers=self.headers)
		try:
			loaded_json = r.json()
		except:
			r.raise_for_status()
		if 'error' in loaded_json:
			error = "[%s] %s"% (loaded_json['error']['id'], loaded_json['error']['text'])
			if 'field' in loaded_json['error']:
				error += " (field: %s)"% loaded_json['error']['field']
			raise self.YelpApiError(error)
		return loaded_json

	
	def get_data(self, lat_long):
		payload = {
			'll':lat_long,
			'radius_filter':200
		}
		loaded_json = self.__request_api(payload)
		total_results = loaded_json['total']
		self.logger.warning("Total venues: %d"% total_results)
		venues = loaded_json['businesses']
		
		nb_venues = len(venues)
		self.logger.info("%d venues now"% nb_venues)
		
		total_results -= nb_venues
		while total_results > 0:
			payload['offset'] = nb_venues
			loaded_json = self.__request_api(payload)
			new_venues = loaded_json['businesses']
			venues += new_venues
			
			nb_venues = len(venues)
			nb_new_venues = len(new_venues)
			self.logger.info("%d more venues => %d venues now"% (nb_new_venues, nb_venues))
			total_results -= nb_new_venues
		
		return venues

		
