from Captor import Captor
import requests
import json

class YahooWeatherCaptor(Captor):
	
	url = "http://query.yahooapis.com/v1/public/yql"
	
	def __get_cleaned_json(self, weather):
		cleaned_loaded_json = {}
		cleaned_loaded_json['lastBuildDate'] = weather['lastBuildDate']
		cleaned_loaded_json['units'] = weather['units']
		cleaned_loaded_json['wind'] = weather['wind']
		cleaned_loaded_json['atmosphere'] = weather['atmosphere']
		cleaned_loaded_json['item'] = {}
		cleaned_loaded_json['item']['condition'] = weather['item']['condition']
		return cleaned_loaded_json
	
	def get_data(self, woe_id):
		payload = {
			'q':"select * from weather.forecast where u='c' and woeid=" + woe_id,
			'format':'json',
			'diagnostics':'true'
		}
		r = requests.get(self.url, params=payload, headers=self.headers)
		if r.status_code <> requests.codes.ok:
			if r.status_code == 999:
				raise UnavailibilityError('YahooWeather', '999', 'Unable to process this request at this time')
			else:
				r.raise_for_status()
		
		loaded_json = json.loads(r.text)
		cleaned_loaded_json = self.__get_cleaned_json(loaded_json['query']['results']['channel'])
		return cleaned_loaded_json
