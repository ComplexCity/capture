from LoggerBuilder import LoggerBuilder
from ExitLogger import ExitLogger
from GitHubDatabaseManager import GitHubDatabaseManager
from GitHubCaptor import GitHubCaptor
import logging
import sqlite3
from datetime import datetime

# Limit: 5000 calls/h => https://developer.github.com/v3/#rate-limiting
source = "github"
logger = LoggerBuilder(source, logging.WARNING, logging.INFO).get_logger()

def main():
	captor = GitHubCaptor(logger)

	try:
		db_conn = sqlite3.connect('github/github.db')
		db_cursor = db_conn.cursor()
		db_manager = GitHubDatabaseManager(logger)

		if db_manager.is_there_user_to_complete(db_cursor):
			logger.info("==== Start to complete users ====")
			limit = captor.get_rate_limit_remaining()
			logger.info("GitHub rate limit remaining: %d calls"% limit)
			if (limit > 0):
				rows = db_manager.get_x_users(db_cursor, limit)
				completed_users = 0
				for row in rows:
					requested_id = row[0]
					requested_login = row[1]
					logger.info("fetching user: %d:%s"% (requested_id, requested_login))
					loaded_user = captor.get_user(requested_login)
					received_id = loaded_user['id']
					if received_id <> requested_id:
						logger.error("The login of user %d has changed")
						db_manager.complete_error_user(db_cursor, requested_id)
					else:
						db_manager.complete_user(db_cursor, loaded_user)
					completed_users += 1
				db_conn.commit()
				logger.info("%d users completed"% completed_users)
		else:
			logger.info("==== Start to fetch new users ====")
			limit = 1
			last_id = db_manager.get_last_id(db_cursor)
			while limit > 0:
				logger.info("Request since: %d", last_id)
				result = captor.get_users(last_id)
				remaining = result['remaining']
				if remaining == None:
					limit -= 1
				last_id = result['since']
				users = result['users']
				inserted_users = 0
				for u in users:
					db_manager.insert_user(db_cursor, u)
					inserted_users += 1
				db_conn.commit()
				logger.info("%d new users inserted"% inserted_users)
		
		db_conn.close()
		return 0

	except Exception, e:
		logger.critical(e, exc_info=True)
		db_conn.close()
		return 1

if __name__ == "__main__":
	start = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	logger.critical("START")
	res = main()
	logger.critical("STOP (%d)"% res)
	stop = datetime.now().strftime('%y-%m-%d %H:%M:%S')
	ExitLogger(source).log(start, stop, res)
	sys.exit(res)