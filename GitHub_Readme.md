##What the script does
The script uses GitHub API to fetch GitHub users' detailed information.
This information is stored in an SQLite database. 

The script can make 2 kinds of work depending on the state of the database:

-	either it fetches new users
-	either it completes the information for previously fetched users (if the database contains some users to complete)

The script request for new users _since_ the last id it received (actually the biggest user id stored in the database). After each request:

-	the script checks the _X-RateLimit-Remaining_ parameter from the GitHub answer to know how many requests it can make
-	the value of _since_ is updated to the last id we got
-	the new users are inserted in the database after each request is treated so that if the script is stopped because a request fails for some reason, then the script can restart without losing everything.

The script stops when the number of remaining requests equals to 0.

The next time the script starts, there will be new users to complete in the database and instead of fetching new users, the script will request detailed information for the new users:

First, the script asks to GitHub how many calls it is allowed and select at most this number of users to complete in the database. For each of this user, the script will:
-	request the information
-	update the user in the database so that if the script is stopped because a request fails for some reason, then the script can restart exactly from where it stopped.

When a user is updated in the database, its _complete_ property becomes true. The commit occurs after the script handled each request, in other word each time a user is updated.

The script also stops when the number of remaining requests equals to 0.

This script could be run hourly.

##Files
###Specific files
-	_GitHubCapture.py_
-	_GitHubCaptor.py_
-	_GitHubDatabaseManager.py_

###Common files
-	_Captor.py_
-	_ExitLogger.py_
-	_LoggerBuilder.py_

###Additional Python modules
-	requests
-	sqlite3

###Logs
-	_./logs/github.log_ for complete logs 
-	_./logs/github-exit.json_ for time and exit status of the last execution
-	_./logs/github-back.json_ for parameters to use when the script is relaunched after error

###Other files and directories
-	_./github/github.db_: the SQLite database


##How to use the script
1.	Copy the files
2.	Create the _logs_ folder
3.	Create the _github_ folder
4.	Create the _github/github.db_ SQLite database and the _User_ table:

		CREATE TABLE User (
			id INTEGER NOT NULL PRIMARY KEY, 
			login TEXT(100,0) NOT NULL, 
			type TEXT(100,0), 
			name TEXT,
			company TEXT,
			blog TEXT,
			location TEXT,
			hireable INTEGER,
			public_repos INTEGER,
			public_gists INTEGER,
			followers INTEGER,
			following INTEGER,
			created_at TEXT(6,0),
			updated_at TEXT(6,0),
			complete INTEGER
		);


5.	Run the script:

		python FoursquareCapture.py
		
##Exit status and Errors
###Exit status
-	**0** in case of **success**

-	**1** in case of a problem with the **database** (e.g. database / table / field not found)

-	**2** in case of a **RequestException** (e.g. network problem, HTTP error, timeout, too many redirections, etc.) different from any GitHub API Error

-	**3** in case of a **GitHub API Error** (see on [GitHub](https://developer.github.com/v3/) for more information) or if the response is not as expected

-	**4** in case of another type of Exception

###Errors
	SQLite3 OperationalError: no such table: Venue
=> See {How to use the script} to create your _foursquare/foursquare.db_

	GitHubApiError: Could not extract the value for since from the GitHub header
<= In the improbable case that the GitHub response is not as expected

	The login of user ID has changed
<= When you request the detailed information of one particular user (identified by his/her login in the request) and that:
-	GitHub answers the user is unknown
-	the user's id in the detailed information received differs from the initial id associated to the user

##Good to know

###FAQ
####Why completing the users just after having new users  instead of fetching all the users first and then complete them all?
The objective is to have the shortest span between these two operations to reduce the risk that a user changes his/her login before we got the complete information. When you request users, in the answer they are uniquely identified by the id. But when you request the detailed information for one specific user you identify this user by the login. This means that if the user changes his/her login, you won't be able to retrieve him/her.

Another reason is that anyway we have to constantly check for new users as new users will continue to sign in. So it seemed a better process to interconnect the 2 tasks in a continuous approach.

####What happens if a user has changed his/her login?
When the script asks for the complete profile of a user, it must use the login. If the user has changed his/her login, we can have 2 situations:

1.	no GitHub user exists any more with the requested login: GitHub will answer with a Not found error.

2.	another GitHub user now have this login and the id of the received profile differs from the id of the user we wanted to complete.

In both situations, the script will simply update the database to say the user doesn't need to be completed anymore and log the error, e.g.:

	ERROR :: The login of user 23 has changed



####How are GitHub HTTP redirects managed?
We're told that API v3 uses HTTP redirection where appropriate and that receiving an HTTP redirection is not an error and clients should follow that redirect (see on [GitHub](https://developer.github.com/v3/) for more information). Nevertheless, the script will handle HTTP redirection with a RequestException.

###Limits
5000 calls/h => [GitHub](https://developer.github.com/v3/#rate-limiting)
