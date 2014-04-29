##What the script does
The script uses Yahoo YQL API to get the weather for big cities.

The script uses the woe_id associated with each city (common with Flickr), e.g.:

-	Paris => [https://www.flickr.com/places/info/12597155](https://www.flickr.com/places/info/12597155)
-	Shanghai => [http://www.flickr.com/places/info/2151849](http://www.flickr.com/places/info/2151849)
-	Beijing => [https://www.flickr.com/places/info/12686916](https://www.flickr.com/places/info/12686916)
-	Tokyo => [https://www.flickr.com/places/info/1118370](https://www.flickr.com/places/info/1118370)
-	New York City => [https://www.flickr.com/places/info/2459115](https://www.flickr.com/places/info/2459115)
-	London => [https://www.flickr.com/places/info/23416974](https://www.flickr.com/places/info/23416974)

The results are written in a JSON file (_YYYY-MM-DD-HH.json_) using the date of the last build of the information (from Yahoo's answer). This way, if the new answer has the same last build date as a previous answer, then the script does not need to write twice the exact same file.

The script could be run hourly.

##Files
###Specific files
-	_YahooWeatherCapture.py_
-	_YahooWeatherCaptor.py_

###Common files
-	_Captor.py_
-	_FileManager.py_
-	_ExitLogger.py_
-	_LoggerBuilder.py_

###Additional Python modules
-	requests

###Logs
-	_./logs/yahooweather.log_ for complete logs 
-	_./logs/yahooweather-exit.json_ for time and exit status of the last execution

###Other files and directories
-	_./yahooweather/_ and the sub-folders for each city where the JSON files will be written
-	_./yahooweather/locations.json_

##How to use the script
1.	Copy the files
2.	Create the _logs_ folder
3.	Create the _yahooweather_ folder and its sub-folders for each city
4.	Create the _yahooweather/locations.json_ file and write a JSON dictionary where the key is the name of the city and the value is the woe_id associated to this city, e.g.:

		{
			"Paris":"12597155",
			"Shanghai":"2151849",
			"Beijing":"12686916",
			"Tokyo":"1118370",
			"NYC":"2459115",
			"London":"23416974"
		}

4.	Run the script:

		python YahooWeatherCapture.py
		
##Exit status and Errors
###Exit status
-	0 in case of success
-	1 in case of an InitError (problem with the _./yahooweather/locations.json_ file or with the _./yahooweather/_ folder or sub-folders)
-	2 in case of a RequestException (e.g. network problem, HTTP error, timeout, too many redirections, etc.)
-	3 in case of another type of Exception

###Errors
	InitError: File ./yahooweather/locations.json is missing
=> You have forgotten to write the _./yahooweather/locations.json_ file

	InitError: The ./yahooweather/locations.json file does not contain any correct JSON object
=> See {How to use the script} to verify that your _./yahooweather/locations.json_ file is correctly written and check that you use " instead of ' for your keys and values.

	InitError: Folder ./yahooweather/{city} is missing
=> You need to create a sub_folder in _/yahooweather/_ for each city

##Good to know
###Information update
How often is the weather information updated => [Yahoo Weather help](http://help.yahoo.com/l/sg/yahoo/weather/general/weather-06.html)
### Limits:
~ 1000 - 2000 calls/h => [YQL FAQ](http://developer.yahoo.com/yql/faq/)
