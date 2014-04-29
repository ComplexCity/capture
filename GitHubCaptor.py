from Captor import Captor
import requests

class GitHubCaptor(Captor):
	
	url_users = "https://api.github.com/users"
	url_rate_limit = "https://api.github.com/rate_limit"
	oauth_client_id = "2f4f86f4263eef17d525"
	oauth_client_secret = "a28d1557d9d5529b5bd3334f53d65d6ea29d8b4b"
	#api_secret = "ace1a8f636d7055f"
	
	class GitHubApiError(Exception):
		pass
	
	def __init__(self, logger):
		self.logger = logger
		
	def __requests_api(self, url, payload):
		r = requests.get(url, params=payload, headers=self.headers)
		print r.url
		try:
			loaded_json = r.json()
		except:
			r.raise_for_status()
		if r.status_code <> requests.codes.ok:
			error = loaded_json['message']
			if 'errors' in loaded_json:
				for error in loaded_json['errors']:
					error += "\n\tfield %s: %s"% (error['field'], error['code'])
			raise self.GitHubApiError(error)
		return {'headers': r.headers, 'loaded_json': loaded_json}
	
	def get_rate_limit_remaining(self):
		payload =  {
			'client_id': self.oauth_client_id,
			'client_secret': self.oauth_client_secret
		}
		loaded_json = self.__requests_api(self.url_rate_limit, payload)['loaded_json']
		return int(loaded_json['rate']['remaining'])
		
	def get_users(self, since):
		payload =  {
			'client_id': self.oauth_client_id,
			'client_secret': self.oauth_client_secret,
			'since': since
		}
		r = self.__requests_api(self.url_users, payload)
		options = r['headers']['Link'].split(';')[0].lstrip('<').rstrip('>').split('?')[1].split('&')
		since = 0
		for option in options:
			if option.startswith('since='):
				since = int(option.lstrip('since='))
		if since == 0:
			raise self. GitHubApiError("Could not extract the value for since from the GitHub header")
		try:
			remaining = int(r['headers']['X-RateLimit-Remaining'])
		except KeyError:
			remaining = None
		return {'remaining': remaining,
			'since': since,
			'users': r['loaded_json']}

	def get_user(self, login):
		payload =  {
			'client_id': self.oauth_client_id,
			'client_secret': self.oauth_client_secret
		}
		return self.__requests_api(self.url_users + "/"+ login, payload)['loaded_json']		