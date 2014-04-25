from Captor import Captor
from UnavailabilityError import UnavailibilityError
import requests
import json

class FlickrCaptor(Captor):
	
	url = "http://api.flickr.com/services/rest/"
	api_key = "2d5481f4b9e0d48f5f3ec89c76ad3dae"
	#api_secret = "ace1a8f636d7055f"
	
	class FlickrApiError(Exception):
		pass
	
	def __init__(self, logger):
		self.logger = logger

	def __get_flickr_json(self, payload):
		r = requests.get(self.url, params=payload, headers=self.headers)
	 	r.raise_for_status()
		
		loaded_json = json.loads(r.text.lstrip('jsonFlickrApi(').rstrip(')'))
		
		if 'code' in loaded_json:
			raise self.FlickrApiError('[code %s] %s'% (loaded_json['code'], loaded_json['message']))
		else:
			return loaded_json

	def __get_cleaned_json(self, photos):
		cleaned_loaded_json = []
		for photo in photos:
			cleaned_photo = {}
			cleaned_photo['id'] = photo['id']
			cleaned_photo['owner'] = photo['owner']
			cleaned_photo['title'] = photo['title']
			cleaned_photo['datetaken'] = photo['datetaken']
			cleaned_photo['latitude'] = photo['latitude']
			cleaned_photo['longitude'] = photo['longitude']
			cleaned_photo['woeid'] = photo['woeid']
			cleaned_photo['place_id'] = photo['place_id']
			cleaned_photo['accuracy'] = photo['accuracy']
			cleaned_photo['context'] = photo['context']
			cleaned_photo['tags'] = photo['tags']
			cleaned_loaded_json.append(cleaned_photo)
		return cleaned_loaded_json

	def get_data(self, min_date, max_date, woe_id):
		payload = {
			'api_key':self.api_key,
			'method':'flickr.photos.search',
			'format':'json',
			'woe_id':woe_id,
			'min_upload_date':min_date,
			'max_upload_date':max_date,
			'extras':'date_taken, geo, tags', 'per_page':'500'}
		loaded_json = self.__get_flickr_json(payload)
		
		total = loaded_json['photos']['total']
		
		cleaned_loaded_json = self.__get_cleaned_json(loaded_json['photos']['photo'])

		pages = loaded_json['photos']['pages']
		if pages > 1:
			self.logger.info("%d pages" % pages)
			for page in range(2, pages+1):
				page_payload = payload
				page_payload['page'] = page
				loaded_json = self.__get_flickr_json(page_payload)
			 	cleaned_loaded_json += self.__get_cleaned_json(loaded_json['photos']['photo'])
		else:
			self.logger.info("1 page")
		return cleaned_loaded_json
					