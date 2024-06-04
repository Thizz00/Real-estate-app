import os
import logging

#Logs
LOG_DIR = 'logs'
LOG_FILE_NAME = 'scraping_log.log'

#Headers for every scrap
HEADERS = {'User-Agent': 'Chrome'}

# Timeouts for every scrap
TIMEOUT = 20


#logs EXISTS

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
log_file_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

#Logs config

logging.basicConfig(level=logging.INFO, filename=log_file_path, format='%(asctime)s [%(levelname)s]: %(message)s')

#Semaphore 
SEMAPHORE_LIMIT = 100 