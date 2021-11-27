#!/usr/bin/python
import urllib.request
import logging
import socket

LOG_LEVEL = logging.INFO
LOG_FILE = "/var/log/freedns"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)

FREEDNS_URL = "http://freedns.afraid.org/dynamic/update.php?"
DOMAIN = "%DOMAINNAMETOBEREPLACED%"
USER_KEY = "%KEYTOBEREPLACED%"

currentip = socket.gethostbyname(DOMAIN)
extip = (urllib.request.urlopen("http://ip.dnsexit.com/").read()).decode().strip()
if currentip != extip:
    try:
        result = urllib.request.urlopen(FREEDNS_URL+USER_KEY).read().decode().strip()
        if result.startswith("ERROR: ") :
            logging.error(result.replace("ERROR: ", ""))
        else:
            logging.info(result)
    except Exception as err:
        logging.error(err)


