##What the script does
The script scraps [http://aqicn.org](http://aqicn.org) mobile page to get the air quality index in big cities.

The results are written in a JSON file (_YYYY-MM-DD-HH.json_).

This script could be run every hour.
##Files
###Specific files
-	_AqiCapture.py_
-	_AqiCaptor.py_
-	_FoursquareDatabaseManager.py_

###Common files
-	_Captor.py_
-	_FileManager.py_
-	_ExitLogger.py_
-	_LoggerBuilder.py_

###Additional Python modules
-	requests
-	lxml

###Logs
-	_./logs/aqi.log_ for complete logs 
-	_./logs/aqi-exit.json_ for time and exit status of the last execution

###Other files and directories

-	_./aqi/_ and the sub-folders for each city where the JSON files will be written
-	_./aqi/locations.json_

##How to use the script
1.	Copy the files
2.	Create the _logs_ folder
3.	Create the _aqi_ folder and its sub-folders for each city
4.	Create the _aqi/locations.json_ file and write a JSON dictionary where the key is the name of the city and the value is the part of the url associated to this city (the ### in http://aqicn.org/city/####/m/), e.g.:

		{
			"Paris":"france/paris/paris-centre",
			"Shanghai":"shanghai",
			"Beijing":"beijing",
			"NYC":"usa/newyork"
		}
 

5.	Run the script:

		python AqiCapture.py
		
##Exit status and Errors
###Exit status
-	0 in case of success
-	1 in case of failure

###Errors
	[Errno 2] No such file or directory: './aqi/locations.json'
	…
=> You have forgotten to write the _./aqi/locations.json_ file


	No JSON object could be decoded
	Traceback (most recent call last):
	  File "AqiCapture.py", line 17, in main
	    locations = file_manager.get_locations(source)
	…
=> Your _./aqi/locations.json_ file is empty or contains no JSON object

	Expecting property name: line 2 column 2 (char 3)
	Traceback (most recent call last):
	  File "AqiCapture.py", line 17, in main
	    locations = file_manager.get_locations(source)
	…
=> See {How to use the script} to verify your _./aqi/locations.json_ file is correctly written and check that you use " instead of ' for your keys and values.

##Good to know
-	The script uses an anonymous user agent to act like a normal browser.

-	For London and Tokyo, I couldn't decide which AQI specific location to use…