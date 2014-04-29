##What the script does
The script fetches Foursquare's venues for big cities.

For each city, it uses a list of locations, e.g.:

-	for Paris, the list of the GPS locations of the centers of each arrondissement and more (for Grand Paris)
-	for Shanghai, the list of the 17 districts

The script requests the venues for each location using the different sections available in the Foursquare's explore query (food, drinks, coffee, shops, arts, outdoors, sights, trending, specials, nextVenues, topPicks). So, for each location, the script makes at least 11 requests (according to the number of the results for one particular section, the script may need more than one request to manage pagination).

For one city, all the venues are temporarily stored in the Venue table of the dedicated SQLite database and one venue is inserted only if it doesn't exist already. This way there is no duplicate for one city.

When all the requests are done for a city, the script writes the json file (_YYYY-MM-DD.json_), empties the Venue table and goes to the next city.

If for some reason, a request fails (e.g. Foursquare stops answering) the script logs in a special file (_foursquare-back.json_) the list the locations the script still needs to request. These locations are used in place of the full list of locations used by default. This is a convenient way to enable the script to restart from where it stopped.

This script could be run daily.

##Files
###Specific files
-	_FoursquareCapture.py_
-	_FoursquareCaptor.py_
-	_FoursquareDatabaseManager.py_

###Common files
-	_Captor.py_
-	_FileManager.py_
-	_ExitLogger.py_
-	_LoggerBuilder.py_

###Additional Python modules
-	requests

###Logs
-	_./logs/foursquare.log_ for complete logs 
-	_./logs/foursquare-exit.json_ for time and exit status of the last execution
-	_./logs/foursquare-back.json_ for parameters to use when the script is relaunched after error

###Other files and directories
-	_./foursquare/_: and the sub-folders for each city where the JSON files will be written
-	_./foursquare/locations.json_
-	_./foursquare/foursquare.db_: the SQLite database


##How to use the script
1.	Copy the files
2.	Create the _logs_ folder
3.	Create the _foursquare_ folder and its sub-folders for each city
4.	Cretae the _foursquare/locations.json_ file and write a JSON dictionary where the key is the name of the city and the value is a list of locations (names or GPS lat/long coordinates), e.g.:
		
		{
			"Paris":[],
			"Shanghai":["Yangpu Qu", "Hongkou Qu", "Zhabei Qu",
				"Putuo Qu", "Changning Qu", "Xuhui Qu", "Jing"an Qu",
				"Huangpu Qu", "Pudong Qu", 	"Baoshan Qu", "Jiading Qu",
				"Qingpu Qu", "Songjiang Qu", "Jinshan Qu", "Fengxian Qu",
				"Minhang Qu", "Chongming Qu"]
		}

5.	Create the _foursquare/foursquare.db_ SQLite database and the _Venue_ table:

		CREATE TABLE Venue (
			id TEXT(50,0) NOT NULL PRIMARY KEY,
			json TEXT NOT NULL
		);


6.	Run the script:

		python FoursquareCapture.py
		
##Exit status and Errors
###Exit status
-	**0** in case of **success**

-	**1** in case of an **InitError** (problem with the _./foursquare/locations.json_ file or with the _./flickr/_ folder or sub-folders)

-	**2** in case of a **RequestException** (e.g. network problem, HTTP error, timeout, too many redirections, etc.) different from any Foursquare API Error

-	**3** in case of a **Foursquare API Error** (see on [Foursquare](https://developer.foursquare.com/overview/responses) for more information)

-	**4** in case of a problem with the **database** (e.g. database / table / field not found)

-	**5** in case of another type of Exception

###Errors
	InitError: File ./foursquare/locations.json file is missing
=> You have forgotten to write the _./foursquare/locations.json_ file

	InitError: The ./foursquare/locations.json file does not contain any correct JSON object
=> See {How to use the script} to verify that your _./foursquare/locations.json_ file is correctly written and check that you use " instead of ' for your keys and values.

	SQLite3 OperationalError: no such table: Venue
=> See {How to use the script} to create your _foursquare/foursquare.db_

##Good to know
###What we understood writing the script
1.	Using calculated GPS locations to make a mesh doesn't seem appropriate as it brought less results than using named places and the script always fails

2.	Using sections increases the results

3.	Foursquare can announce a total of 14 results to a request and send only 13 venues so the script checks if, considering the pagination limit, all the results should have been received and continues to request venues only if it is not the case.

###Limits
5000 calls/h => [Foursquare](https://developer.foursquare.com/overview/ratelimits)
