import logging
import datetime

LOG_FILENAME = 'system.log'

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def write(text):
    now = datetime.datetime.now()
    logging.debug(' - ' + str(now) + ' - ' + text)
