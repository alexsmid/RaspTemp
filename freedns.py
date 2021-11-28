#!/usr/bin/python
import urllib.request
import logging
import os

LOG_LEVEL = logging.INFO
HOME = os.environ.get('HOME')
LOG_FILE = os.path.join(HOME,"RaspTemp/freedns.log")
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
OLDIP_FILE = os.path.join(HOME, "RaspTemp/freedns.oldip")

FREEDNS_URL = "http://freedns.afraid.org/dynamic/update.php?"
DOMAIN = "%DOMAINNAMETOBEREPLACED%"
USER_KEY = "%KEYTOBEREPLACED%"

extip = (urllib.request.urlopen("http://ip.dnsexit.com/").read()).decode().strip()

def writeiptofile(ip):
    f = open(OLDIP_FILE, 'w')
    f.write(extip)
    f.close()

def updatedns(extip):
    try:
        result = urllib.request.urlopen(FREEDNS_URL+USER_KEY).read().decode().strip()
        if result == "ERROR: Address " + extip + " has not changed.":
            writeiptofile(extip)
            logging.error(result.replace("ERROR: ", ""))
        elif result.startswith("ERROR: ") :
            logging.error(result.replace("ERROR: ", ""))
        else:
            writeiptofile(extip)
            logging.info(result)
    except Exception as err:
        logging.error(err)

if not os.path.exists(OLDIP_FILE):
    updatedns(extip)
else:
    f = open(OLDIP_FILE, 'r')
    oldip = f.read()
    f.close()
    if oldip != extip:
        updatedns(extip)

