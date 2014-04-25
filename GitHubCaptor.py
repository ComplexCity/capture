from Captor import Captor
from UnavailabilityError import UnavailibilityError
import requests

class GitHubCaptor(Captor):
	
	url_users = "https://api.github.com/users"
	url_rate_limit = "https://api.github.com/rate_limit"
	oauth_client_id = "2f4f86f4263eef17d525"
	oauth_client_secret = "a28d1557d9d5529b5bd3334f53d65d6ea29d8b4b"
	#api_secret = "ace1a8f636d7055f"
	
	def __init__(self, logger):
		self.logger = logger

	def get_rate_limit_remaining(self):
		payload =  {
			'client_id': self.oauth_client_id,
			'client_secret': self.oauth_client_secret
		}
		r = requests.get(self.url_rate_limit, params=payload, headers=self.headers)
		r.raise_for_status()
		loaded_json = r.json()
		return int(loaded_json['rate']['remaining'])
		
	def get_users(self, since):
		payload =  {
			'client_id': self.oauth_client_id,
			'client_secret': self.oauth_client_secret,
			'since': since
		}
		r = requests.get(self.url_users, params=payload, headers=self.headers)
		r.raise_for_status()
		options = r.headers['Link'].split(';')[0].lstrip('<').rstrip('>').split('?')[1].split('&')
		since = 0
		for option in options:
			if option.startswith('since='):
				since = int(option.lstrip('since='))
		if since == 0:
			self.logger.error("Could not extract the value for since from the GitHub header")
		try:
			remaining = int(r.headers['X-RateLimit-Remaining'])
		except KeyError:
			remaining = None
		loaded_json = r.json()
		return {'remaining': remaining,
			'since': since,
			'users': loaded_json}

	def get_user(self, login):
		payload =  {
			'client_id': self.oauth_client_id,
			'client_secret': self.oauth_client_secret
		}
		r = requests.get(self.url_users + "/"+ login, params=payload, headers=self.headers)
	 	r.raise_for_status()
		return json.loads(r.text)		