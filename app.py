#!/usr/bin/python

import threading
import time
import logging
import os
import requests
import platform
from flask import Flask, jsonify, request

application = Flask(__name__)
logger = logging.getLogger(__name__)
#Amount to time to sleep, prior to starting web.  This is intended to simulate
#applicaiton startup or deployment
init_sleep=10
#This is intended to signal that the applicaiton is up and healthy.
#If the file does not exist, one can assume that the app is starting, or dead
status_file='/tmp/status.up'

sample_json='{ "message" : "test" }'


@application.route("/")
def hello():
    #Simple service endpoint to acknowledge
    return platform.node()

@application.route("/healthz")
def healthz():
    #Ideally this would contain logic provided by the developer as to
    #what requirements are necessary for the application to be up.
    #i.e. database connection, queue connection, service connection, etc
    return "OK\r\n"

@application.route("/env")
def env():
    return os.environ['DEPLOY_ENV']

@application.route('/badhealthz')
def badhealtz():
    #Endpoint for a bad health check, just return a HTTP error code > 400
    abort(418)

@application.route('/crash')
def crash():
    #This endpoint is intended to simulate an app crash.
    #To do this we just remove the applicaiton status file
    #logger.info("Deleting file: %s to simulate application crash.", status_file)
    os.remove(status_file)
    return "Your request to crash the app has been accepted.\r\n"

#This function just waits for the web process to start, and when a HTTP 200
#is returned the status file is created.
def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get('http://0.0.0.0:8080/')
                if r.status_code == 200:
                    #logger.info("Server started, creating status file at: %s", status_file)
                    if not os.path.exists(status_file):
                        os.mknod(status_file)
                    not_started = False
                print(r.status_code)
            except:
                err = True
                #logger.info('Server not yet started')
            time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()

#App entry point.
if __name__ == "__main__":

    #Create a logger
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
    logging.basicConfig(format='%(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
    logger.info("==========================================================")
    logger.info("Starting Sample Python Web Applicaiton")
    logger.info("Sleeping for %s seconds", init_sleep)
    #Sleep the app to simulate a startup lag
    time.sleep(init_sleep) # delays for 60 seconds
    logger.info("Sleep Ended")
    logger.info(sample_json)
    #Execute the thread to create the status file.
    start_runner()

    #Finally start the web process and list on 8080 all IP addresses
    application.run(host='0.0.0.0', port=8080)
