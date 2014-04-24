from Captor import Captor
import requests
from lxml import html

class AqiCaptor(Captor):
	
	url = "http://aqicn.org/city/##/m/"
	
	def __init__(self, logger):
		self.logger = logger
		
	def get_data(self, location):
		scrapped_url = self.url.replace("##", location)
		self.logger.info("scrapped_url=%s"% scrapped_url)
		r = requests.get(scrapped_url, headers=self.headers_anonymous)
		r.raise_for_status()
		tree = html.fromstring(r.text)
		data = {
			'pm25': tree.xpath('//td[@id="cur_pm25"]/div/text()'),
			'pm10': tree.xpath('//td[@id="cur_pm10"]/div/text()'),
			'o3': tree.xpath('//td[@id="cur_o3"]/div/text()'),
			'no2': tree.xpath('//td[@id="cur_no2"]/div/text()'),
			'so2': tree.xpath('//td[@id="cur_so2"]/div/text()'),
			'co': tree.xpath('//td[@id="cur_co"]/div/text()'),
			'temperature': tree.xpath('//td[@id="cur_t"]/div/text()'),
			'dew': tree.xpath('//td[@id="cur_d"]/div/text()'),
			'pressure': tree.xpath('//td[@id="cur_p"]/div/text()'),
			'humidity': tree.xpath('//td[@id="cur_h"]/div/text()'),
			'wind': tree.xpath('//td[@id="cur_w"]/div/text()')
		}
		return data
		