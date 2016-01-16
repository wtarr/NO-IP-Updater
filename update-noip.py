#!/usr/local/bin/python

#script maintains a cache of the latest user ip address
#updates to no-ip occur only on a detected change
#
#script was created for running as a cron job

import requests, logging

HOSTNAME = ""
USERNAME = ""
PASSWORD = ""

updateurl = "https://dynupdate.no-ip.com/nic/update?hostname={hostname}&myip={ip}"

getipurl = "https://api.ipify.org" 

# http://ipinfo.io/ip

# set up logging
logging.basicConfig(level=logging.INFO,
        filename='/root/no-ip/noip-update-log.log',
        format='%(asctime)s %(message)s')

# fetch current Ip address
logging.info("===== Begin =====")
logging.info("fetching the current ip address")
current = requests.get(getipurl)
logging.info("public ip {}".format(current.text))
if (current.status_code == 200):
    # open existing dat file containing current ip address  
    logging.info("open stored ip address")
    f = open("/root/no-ip/ip.dat")

    # read all the lines in the file and return them in a list
    lines = f.readlines()
  
    f.close()

    if lines[0] == current.text:
        logging.info("current: {} and stored {} are the same no need to update".format(current.text.strip(), str.rstrip(lines[0])))
    else:
        logging.info("begin updating to no-ip")
        url_formatted = updateurl.format(hostname=HOSTNAME, ip=current.text)

        req = requests.get(url_formatted, auth=(USERNAME, PASSWORD))
        logging.info("Status code from no-ip: {}".format(req.status_code))
        fi = open('/root/no-ip/ip.dat', 'w')        
        # replace with new/current ip
        fi.write(current.text)
        fi.close()
else:
        logging.info("Status code for ip lookup did not return 200 OK")
logging.info("===== End =====")        








