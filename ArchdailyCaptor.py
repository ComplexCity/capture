from Captor import Captor
import requests
from lxml import html
import json

class ArchdailyCaptor(Captor):
	
	url = "http://www.archdaily.com/map/"
	
	def get_data(self):
		result = []
		r = requests.get(self.url, headers=self.headers_anonymous)
		r.raise_for_status()
		tree = html.fromstring(r.text)
		script = tree.xpath('//div[@id="main"]/script/text()')[0]
		lines = script.split('\n')
		for line in lines:
			line = line.strip()
			if line.startswith('markers_info') and line.endswith('};'):
				line = line.split('] = ')[1]
				line = line.replace('};', '}')
				line = line.replace("\\'", "'").replace("\\", " ").replace("\"", "\\\"").replace("\t", " ")
				line = line.replace(":'", ":\"").replace("',", "\",").replace("' }", "\" }")
				line = line.replace('title:', "\"title\":")
				line = line.replace('href:', "\"href\":")
				line = line.replace('src:', "\"src\":")
				line = line.replace('address:', "\"address\":")
				line = line.replace('lat:', "\"lat\":")
				line = line.replace('lng:', "\"lng\":")
				try:
					loaded_json = json.loads(line)
				except ValueError:
					print line
					raise
				result.append(loaded_json)	
		return result
		