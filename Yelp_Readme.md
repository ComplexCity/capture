##What the script does
The script fetches Yelp's venues for big cities.

For each city, it uses a list of locations, e.g.:

-	for Paris, the list of the GPS locations of the centers of each arrondissement and more (for Grand Paris)

For one city, all the venues are temporarily stored in the Venue table of the dedicated SQLite database and one venue is inserted only if it doesn't exist already. This way there is no duplicate for one city.

When all the requests are done for a city, the script writes the json file (_YYYY-MM-DD.json_), empties the Venue table and goes to the next city.

If for some reason, a request fails (e.g. Yelp stops answering) the script logs in a special file (_yelp-back.json_) the list of locations the script still needs to request. These locations are used in place of the full list of locations used by default. This is a convenient way to enable the script to restart from where it stopped.

This script could be run daily.

##Files
###Specific files
-	_YelpCapture.py_
-	_YelpCaptor.py_
-	_YelpDatabaseManager.py_

###Common files
-	_Captor.py_
-	_FileManager.py_
-	_ExitLogger.py_
-	_LoggerBuilder.py_

###Additional Python modules
-	requests
-	requests_oauthlib

###Logs
-	_./logs/yelp.log_ for complete logs 
-	_./logs/yelp-exit.json_ for time and exit status of the last execution
-	_./logs/yelp-back.json_ for parameters to use when the script is relaunched after error

###Other files and directories
-	_./yelp/_: and the sub-folders for each city where the JSON files will be written
-	_./yelp/locations.json_
-	_./yelp/yelp.db_: the SQLite database


##How to use the script
1.	Copy the files
2.	Create the _logs_ folder
3.	Create the _yelp_ folder and its sub-folders for each city
4.	Cretae the _yelp/locations.json_ file and write a JSON dictionary where the key is the name of the city and the value is a list of locations (GPS lat/long coordinates), e.g.:
		
		{
			{"Paris":["48.8618, 2.3477","48.8644, 2.3385","48.8605, 2.3380"]}
		}

5.	Create the _yelp/yelp.db_ SQLite database and the _Venue_ table:

		CREATE TABLE Venue (
			id TEXT(50,0) NOT NULL PRIMARY KEY,
			json TEXT NOT NULL
		);


6.	Run the script:

		python YelpCapture.py
		
##Exit status and Errors
###Exit status
-	**0** in case of **success**

-	**1** in case of an **InitError** (problem with the _./yelp/locations.json_ file or with the _./yelp/_ folder or sub-folders)

-	**2** in case of a **RequestException** (e.g. network problem, HTTP error, timeout, too many redirections, etc.) different from any Foursquare API Error

-	**3** in case of a **Yelp API Error** (see on [Yelp](http://www.yelp.com/developers/documentation/v2/errors) for more information)

-	**4** in case of a problem with the **database** (e.g. database / table / field not found)

-	**5** in case of another type of Exception

###Errors
	InitError: File ./yelp/locations.json file is missing
=> You have forgotten to write the _./yelp/locations.json_ file

	InitError: The ./yelp/locations.json file does not contain any correct JSON object
=> See {How to use the script} to verify that your _./yelp/locations.json_ file is correctly written and check that you use " instead of ' for your keys and values.

	SQLite3 OperationalError: no such table: Venue
=> See {How to use the script} to create your _yelp/yelp.db_

##Good to know

###Limits
10000 calls/day => [Yelp](http://www.yelp.com/developers/documentation/faq#q2)
