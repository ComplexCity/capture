from Captor import Captor
import requests
from requests_oauthlib import OAuth1

class YelpCaptor(Captor):
	
	url = "http://api.yelp.com/v2/search"

#	api_v1_ywsid = "8wN7f46VHLdBffdCnDqPQg"
	oauth_consumer_key = "znJD_ORvGMYy_eIaJ2_snA"
	oauth_consumer_secret = "kuzBopIN_U4ANGAkgQQG5r_bSW8"
	oauth_token = "04dZGXX08XOhT63Spn3bo65iidBq6LLN"
	oauth_token_secret = "Fb5TbmK6ruu2xiezlqVSGNcMyms"

	def __init__(self, logger):
		self.logger = logger
	
	def get_data(self, lat_long):
		payload = {
			'll':lat_long,
			'radius_filter':200
		}
		auth = OAuth1(self.oauth_consumer_key,
					  client_secret=self.oauth_consumer_secret,
					  resource_owner_key=self.oauth_token,
					  resource_owner_secret=self.oauth_token_secret,
					  signature_type='query')
		r = requests.get(self.url, params=payload, auth=auth, headers=self.headers)
		r.raise_for_status()
		loaded_json = r.json()
		total_results = loaded_json['total']
		self.logger.warning("Total venues: %d"% total_results)
		venues = loaded_json['businesses']
		
		nb_venues = len(venues)
		self.logger.info("%d venues now"% nb_venues)
		could_take_all = False
		if total_results <= self.limit:
			could_take_all = True
		total_results -= nb_venues
		while total_results > 0 and could_take_all == False:
			payload['offset'] = nb_venues
			r = requests.get(self.url, params=payload, auth=auth, headers=self.headers_anonymous)
			r.raise_for_status()
			loaded_json = r.json()
			new_venues = loaded_json['businesses']
			venues += new_venues
			
			nb_venues = len(venues)
			nb_new_venues = len(new_venues)
			self.logger.info("%d more venues => %d venues now"% (nb_new_venues, nb_venues))
			if total_results <= self.limit:
				could_take_all = True
			else:
				total_results -= nb_new_venues
		
		return venues

		