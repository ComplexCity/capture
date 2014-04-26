#Flickr Capture
##What the script does
The script uses Flickr API (search) to fetch Flickr's photos located in big cities.

The script uses the woe_id associated with each city, e.g.:

-	Paris => [https://www.flickr.com/places/info/12597155](https://www.flickr.com/places/info/12597155)
-	Shanghai => [http://www.flickr.com/places/info/2151849](http://www.flickr.com/places/info/2151849)
-	Beijing => [https://www.flickr.com/places/info/12686916](https://www.flickr.com/places/info/12686916)
-	Tokyo => [https://www.flickr.com/places/info/1118370](https://www.flickr.com/places/info/1118370)
-	New York City => [https://www.flickr.com/places/info/2459115](https://www.flickr.com/places/info/2459115)
-	London => [https://www.flickr.com/places/info/23416974](https://www.flickr.com/places/info/23416974)

At the beginning the script reads the _./flickr/min_date.json_ file to get the date since when the photos must be fetched.

While this date is strictly before yesterday, the script enters a loop to:
- request the photos __uploaded__ on this date for each city and writes the result in a JSON file (_YYYY-MM-DD.json_) (one JSON file by city)
- adds one day to the date and write this new date in the _./flickr/min_date.json_ file

This way, when the script stops (normally or if, for some reason, a request fails), the _./flickr/min_date.json_ file is already updated with the next date to be used to fetched the photos.

This script could be running continuously while the date is strictly before the day before yesterday (it sleeps for 5s between 2 dates) and then it could be run daily.

##Files
###Specific files
-	_FlickrCapture.py_
-	_FlickrCaptor.py_

###Common files
-	_Captor.py_
-	_FileManager.py_
-	_UnavailibilityError.py_
-	_ExitLogger.py_
-	_LoggerBuilder.py_

###Additional Python modules
-	Requests

###Logs
-	_./logs/flickr.log_ for complete logs 
-	_./logs/flickr-exit.json_ for time and exit status of the last execution

###Other files and directories
-	_./flickr/_ and the sub-folders for each city where the JSON files will be written
-	_./flickr/min_date.json_: the JSON file where to set the date since when the photos must be fetched
-	_./flickr/locations.json_

##How to use the script
1.	Copy the files
2.	Create the _logs_ folder
3.	Create the _flickr_ folder and its sub-folders for each city
4.	Create the _flickr/min_date.json_ file and edit it to set the date since when the photos must be fetched:

		{"min_date":"YYYY-MM-DD"} 

5.	Create the _flickr/locations.json_ file and write a JSON dictionary where the key is the name of the city and the value is the woe_id associated to this city, e.g.:

		{
			"Paris":"12597155",
			"Shanghai":"2151849",
			"Beijing":"12686916",
			"Tokyo":"1118370",
			"NYC":"2459115",
			"London":"23416974"
		}

6.	Run the script:

		python FlickrCapture.py
		
##Exit status and Errors
###Exit status
-	**0** in case of **success**

-	**1** in case of an **InitError** (problem with the _./flickr/locations.json_ or _./flickr/min_date.json_ files or with the _./flickr/_ folder or sub-folders)

-	**2** in case of a **RequestException** (e.g. network problem, HTTP error, timeout, too many redirections, etc.)

-	**3** in case of a **Flickr API Error** (see on [Flickr](https://www.flickr.com/services/api/response.json.html) for more information)

-	**4** in case of another type of Exception


###Errors
	InitError: File ./flickr/locations.json file is missing
=> You have forgotten to write the _./flickr/locations.json_ file

	InitError: The ./flickr/locations.json file does not contain any correct JSON object
=> See {How to use the script} to verify that your _./flickr/locations.json_ file is correctly written and check that you use " instead of ' for your keys and values.

	InitError: File ./flickr/min_date.json is missing. You should create this file and set {'min_date':YYYY-MM-DD} in it.
=> You have forgotten to write the _./flickr/min_date.json_ file

	InitError: You need to set {\"min_date\":\"YYYY-MM-DD\"} in file ./flickr/min_date.json
=> See {How to use the script} to verify that your _./flickr/min_date.json_ file is correctly written and check that you use " instead of ' for your keys and values.

	InitError: The date set as min_date in ./flickr/min_date.json is after 2 days ago.
=> Set the date before yesterday

	InitError: Folder ./flickr/{city} is missing
=> You need to create a sub_folder in _/flickr/_ for each city

##Good to know
### FAQ
####Why using the uploaded date instead of the taken date?
Because after the end a day, the photos uploaded on this day are already all there so we can fetch them once and be sure the job is well and truly done.
On the contrary, photos taken on this day can be uploaded to Flickr on the same day or anytime in the future. So if we used the taken date, there would be no way for us to be sure that we have fetched all the photos taken on a this date.

####Why fetching photos uploaded 2 days ago is the most recent request the script allows?
The objective is to be able to fetch all the photos uploaded to Flickr on a certain day at once. So we must be sure the whole day has passed everywhere around the world considering the time offset.

###Limits
-	For Limit for Flickr API: 3600 queries / h => [Flickr API](http://www.flickr.com/services/developer/api/)

-	For flickr.photos.search: Flickr will return at most the first 4,000 results for any given search query.

---
#Flickr GeoJSON Building
##What the script does
The script creates GeoJSON files from JSON files created by the Capture script:
-	.geojson file
-	.js file, a JavaScript version of the .geojson file so it can be used directly with Leaflet

##Files
###Specific files
-	_FlickrGeojsonBuilding.py_
-	_FlickrGeojsonBuilder.py_

###Common files
-	_GeojsonBuilding.py_
-	_GeojsonBuilder.py_
-	(_FileManager.py_, already in use for the Capture)

###Logs
Only a stream handler is added to the logger.

###Other files and directories
The script will write the geojson files at the same place as it finds the primitive json files, that is to say in the sub-folders of _./flickr/_.

##How to use the script
1.	Copy the files
2.	Run the script:

		python FlickrGeojsonBuilding.py
		
##Exit status and Errors
###Exit status
-	0 in case of success
-	1 in case of failure
